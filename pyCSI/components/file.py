"""
=====
PyCSI File component
=====

The File component gives access to the model CSI API File Interface
"""

import os
from pathlib import Path
from typing import Optional

from pyCSI.protocols import IFile
from pyCSI.protocols import BaseModel
from pyCSI.utils import check_request


class File:
    """File component class of the model object.

    Args:
        model_object (Model): Instance of a PyCSI Model class.
    """

    def __init__(self, parent) -> None:
        self._parent: BaseModel = parent
        self._file: IFile = parent.get_model_object().File

    def open_file(self, file: Path | str) -> None:
        """Opens an existing model file.

        Args:
            file_name: The path of the model file to be opened.
        """

        if isinstance(file, Path):
            file = str(file)

        # Check that the specified file exists
        if not os.path.isfile(file):
            raise FileNotFoundError(f'File {file} not found')

        return_code = self._file.OpenFile(file)
        check_request(return_code)
        print(f'Successfully connected to {self._parent.get_file_name()}')

    def new_model(self):
        """Initialize a new model on the active api object"""

        model_object = self._parent.get_model_object()
        return_code: int = model_object.InitializeNewModel()
        check_request(return_code)

    def save(self, file_name: Optional[str] = None, path: Optional[Path | str] = None) -> None:
        """Saves the model with the specified path and file name.

        Args:
            file_name: New name to save the model. If not provided, the model 
            is saved using the current name. If the file has not been saved
            previously and file_name is omitted an error will be raised.
            Defaults to None.

            path: The full path to where the model will be saved. If not 
            provided, the model is saved in the current location. Defaults
            to None.
        """

        # If file_name and path are not provided save to current location
        if file_name is None and path is None:
            return_code = self._file.Save()
            check_request(return_code)
            return

        # If path is not provided get current path
        if path is None:
            path = self._parent.get_file_path()

        # Check that path exists
        if isinstance(path, str):
            path = Path(path)
        if not path.is_dir():
            raise OSError(f'Specified {path = } does not exists')

        # If file_name is not provided get current name
        if file_name is None:
            file_name = self._parent.get_file_name()

        # Concatenate full name and save the model
        full_name = path.joinpath(file_name)
        return_code = self._file.Save(str(full_name))
        check_request(return_code)
