"""
=====
PyCSI Groups component
=====

The Group component gives access to the model CSI API Group Interface
"""

import pandas as pd

from pyCSI.protocols import IModel
from pyCSI.utils import check_request


class Groups:
    """Group component of the Model Class.

    Args:
        parent (Model): Instance of a PyCSI Model class.
    """

    def __init__(self, parent) -> None:
        self._parent = parent
        self._model_object: IModel = parent.get_model_object()

    def create(self, group_name: str):
        """Defines a new group definition"""

        return_code = self._model_object.GroupDef.SetGroup_1(group_name)
        check_request(return_code)

    def get_names(self) -> list[str]:
        """Gets a list of all defined groups in the model"""

        request_result = self._model_object.GroupDef.GetNameList()
        return_code = request_result[-1]
        check_request(return_code)  # Check API request
        return request_result[1]

    def add_object_from_name(self, unique_name: str, object_type: str, group_name: str,
                             replace_group: bool = False, remove: bool = False):
        """Adds objects to a group specifying its unique name and object type.

        Args:
            unique_name: Object unique name in string format.
            object_type: Object type in string format.
            Accepted values are:
            - frame
            - area
            - joint
            - link

            group_name: Name of the group to be modified.

        Keyword Args:
            replace_group: If `True`, the specified objects will replace the group.
            Otherwise, objects will be added to the group. Defaults to `False`.
            remove: If `True`, objects will be removed from specified group.
            Defaults to `False`.
        """

        object_functions = {'frame': self._model_object.FrameObj.SetGroupAssign,
                            'area': self._model_object.AreaObj.SetGroupAssign,
                            'joint': self._model_object.PointObj.SetGroupAssign,
                            'link': self._model_object.LinkObj.SetGroupAssign}

        # Check that object type format is consistent
        object_type = object_type.lower()

        # Check that object types is valid
        if not object_type in object_functions:
            raise ValueError(
                f'Object type {object_type} for object {unique_name} is not valid. \
                Valid types are frame, area, joint and link')

        # If replace_group, delete and redefine group
        if replace_group:
            self._model_object.GroupDef.Delete(group_name)

        # Check if group exists in the model, if not create it
        if group_name not in self.get_names():
            self.create(group_name)

        # Add object to group
        object_function = object_functions[object_type]
        return_code = object_function(str(unique_name), group_name, remove)
        check_request(return_code)

    def add_objects_from_dataframe_names(self, objects: pd.DataFrame, group_name: str, **kwargs):
        """Add objects to a group from a DataFrame specifying its unique name
        and object type.

        Args:
            objects: A two column Dataframe containing the following:
            - unique_name (str): Object's unique name.
            - object_type (str): Object type. See `add_object_from_name()` 
            for valid object types.

            group_name: Name of the group to be modified.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword
            arguments.
        """

        # Check the DataFrame is not empty
        if objects.shape[0] == 0:
            raise ValueError('No objects added to group')

        # Check the size of the provided DataFrame
        if not objects.shape[1] == 2:
            raise ValueError(
                '''Objects DataFrame shape is not valid.
                Objects must contain a two-column DataFrame with the
                object\'s unique name and type''')

        for i, _object in objects.iterrows():
            unique_name = _object.iloc[0]
            object_type = _object.iloc[1]
            if i == 0:
                # Replace group only for the first object of the dataframe
                self.add_object_from_name(unique_name, object_type, group_name, **kwargs)
            else:
                remove = kwargs['remove']
                self.add_object_from_name(unique_name, object_type, group_name, remove=remove)

    def add_objects_of_same_type_from_dataframe_names(self, unique_names: pd.DataFrame, group_name: str,
                                                      object_type: str, **kwargs):
        """Add objects of the same type to a group from a DataFrame specifying
        its unique name.

        Args:
            unique_names: Single column Dataframe containing the object's unique
            name in string format.

            group_name: Name of the group to be modified.

            object_type: Object type in string format. See `add_object_from_name()`
            for valid object types.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword 
            arguments.
        """

        # Check the size of the provided DataFrame
        if not unique_names.shape[1] == 1:
            raise ValueError(
                '''Unique Names DataFrame shape is not valid.
                Unique Names must contain a single-column DataFrame 
                with the object\'s unique name''')

        # Add a second column to the unique_names DataFrame with the object type
        unique_names['types'] = object_type

        # Add to group
        self.add_objects_from_dataframe_names(unique_names, group_name, **kwargs)

    def add_objects_from_clipboard_names(self, group_name: str, wait_for_user: bool = False, **kwargs):
        """Add objects to a group specifying its unique name and object type.

        Note:
            This function requires the user to copy into the clipboard a two-column
            dataset containing the following:

            - unique_name: Object unique name in string format
            - object_type: Object type in string format. See `add_object_from_name()`
            for valid object types.

        Args:
            group_name: Name of the group to be modified.

            wait_for_user: If `True`, the program will pause before executing
            the function to allow the user to copy into the clipboard the
            dataset. Defaults to `False`.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword 
            arguments.
        """

        if wait_for_user:
            # Let user copy the dataset
            print(f'Adding to objects to {group_name}')
            print('Copy into your clipboard the objects to add')
            _ = input('Press Enter to continue...')

        # Read objects from clipboard
        objects = pd.read_clipboard(header=None)

        # Add objects to group
        self.add_objects_from_dataframe_names(objects, group_name, **kwargs)

    def add_objects_of_same_type_from_clipboard_names(self, group_name: str, object_type: str, **kwargs):
        """Add objects of the same type to a group specifying its unique name.

        Note:
            This function requires the user to copy into the clipboard a single 
            column dataset containing the object's unique name in string format.

        Arguments:
            group_name: Name of the group to be modified.
            object_type: Object type  in string format. See `add_object_from_name()`
                for valid object types.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword 
            arguments.
        """

        # Read objects from clipboard
        objects = pd.read_clipboard(header=None)

        # Add objects to group
        self.add_objects_of_same_type_from_dataframe_names(objects, group_name, object_type, **kwargs)

    def add_object_from_label(self, label: str, story: str, group_name: str, **kwargs):
        """Add object to a group specifying its label and story

        Arguments:
            label: Object's label.
            story: Object's story.
            group_name: Name of the group to be modified.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword 
            arguments.
        """

        # Get object unique name
        unique_name, object_type = self._get_unique_name_from_label(label, story)

        # Add object to group
        self.add_object_from_name(unique_name, object_type, group_name, **kwargs)

    def add_objects_from_dataframe_labels(self, objects: pd.DataFrame, group_name: str, **kwargs):
        """Add objects to a group from a DataFrame specifying its label and story.

        Args:
            objects: A two column Dataframe containing the following:

            - label (str): Object's label.
            - story (str): Object's story.

            group_name: Name of the group to be modified.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword 
            arguments.
        """
        # Check the DataFrame is not empty
        if objects.shape[0] == 0:
            raise ValueError('No objects added to group')

        # Check the size of the provided DataFrame
        if not objects.shape[1] == 2:
            raise ValueError(
                '''Objects DataFrame shape is not valid.
                Objects must contain a two-column DataFrame 
                with the object\'s label and story''')

        # Get objects unique names
        objects = self._get_unique_names_from_dataframe_labels(objects)

        # Add objects to group
        self.add_objects_from_dataframe_names(objects, group_name, **kwargs)

    def add_objects_from_clipboard_labels(self, group_name: str, **kwargs):
        """Add objects to a group specifying its label and story.

        Note:
            This function requires the user to copy into the clipboard a two-column
            dataset containing the following:

            - label: Object label in string format.
            - story: Object story in string format.

        Arguments:
            group_name: Name of the group to be modified.

        Keyword Args:
            **kwargs: See `.add_object_from_name()` for remaining keyword 
            arguments.
        """

        # Read objects from clipboard
        objects = pd.read_clipboard(header=None)

        # Add objects to group
        self.add_objects_from_dataframe_labels(objects, group_name, **kwargs)

    ###################################################################################################################
    # Miscellaneous Methods
    ###################################################################################################################

    def _get_object_type(self, label: str):
        # Gets the type of an object based on its label

        # Validate that label is in string format
        label = label.upper()
        if not isinstance(label, str):
            raise ValueError(f'Label {label} is not in string format')

        # Area objects
        if label.startswith(('F', 'W', 'A')):
            return 'area'

        # Frame objects
        if label.startswith(('B', 'C', 'L', 'D')):
            return 'frame'

        if label.isdigit():
            return 'joint'

        # If label does not match any of the above raise an error
        raise ValueError(f'Label {label} does not match any of the object types')

    def _get_unique_name_from_label(self, label: str, story: str) -> tuple[str, str]:
        # Gets the unique name of an object base on its label and story.

        # Object function
        object_functions = {'frame': self._model_object.FrameObj.GetNameFromLabel,
                            'area': self._model_object.AreaObj.GetNameFromLabel,
                            'joint': self._model_object.PointObj.GetNameFromLabel}

        # Get object type from label
        object_type = self._get_object_type(label)

        # Get unique name
        object_function = object_functions[object_type]
        request = object_function(label, story)
        check_request(request[-1])

        return request[0], object_type

    def _get_unique_names_from_dataframe_labels(self, objects: pd.DataFrame) -> pd.DataFrame:
        # Gets the unique names of the specified objects based on its labels and stories

        # Get unique name and object type for each object
        unique_names = []
        object_types = []
        for _, _object in objects.iterrows():
            unique_name, object_type = self._get_unique_name_from_label(_object.iloc[0], _object.iloc[1])
            unique_names.append(unique_name)
            object_types.append(object_type)

        objects_names = {'name': unique_names, 'type': object_types}
        return pd.DataFrame(objects_names)
