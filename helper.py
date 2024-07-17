"""
=====
PyCSI Helper class
=====

This class gives access to the CSI API Helper Interface
"""


from typing import cast
from typing import Optional

from comtypes.client import CreateObject

from pyCSI.protocols import IHelper
from pyCSI.protocols import IApi


class Helper:
    """CSI API Helper Object class

    Args:
        clsid: Class ID that represents the API Object to be created. 

    Note:
        Valid CLIDs are:
        - ETABS: 'CSI.ETABS.API.ETABSObject'.
        - SAP2000: 'CSI.SAP2000.API.SapObject'.
        - SAFE: 'CSI.SAFE.API.ETABSObject'.
    """

    HELPER_CLSID = 'CSiAPIv1.Helper'

    def __init__(self, clsid: str) -> None:
        # Use cast function to assign helper object as type IHelper
        helper_object = cast(IHelper, CreateObject(self.HELPER_CLSID))
        self.helper = helper_object
        self.clsid: str = clsid

    def get_api_object(self, pid: Optional[int] = None) -> IApi | None:
        """Gets a running API Object. If a PID is provided, returned API object
        will be the one with the specified process ID, otherwise, returned API
        Object will be the currently active one.

        Args:
            pid: The system-generated unique identifier (process ID) of the
            desired instance of the program. See PID number under software\'s
            `Tools` menu.

        Returns:
            APIObject if successful, otherwise None
        """

        if pid is None:
            # Attach to the active instance in the ROT
            return self.helper.GetObject(self.clsid)

        # Attach to the instance with the given process ID
        return self.helper.GetObjectProcess(self.clsid, pid)

    def create_api_object(self, api_path: Optional[str] = None) -> IApi | None:
        """Creates a new instance of the API Object.

        Args:
            api_path: Path to the API executable. Defaults to None.

        Returns:
            APIObject if successful, otherwise None.
        """

        if api_path is None:
            # Creates the default API Object
            return self.helper.CreateObjectProgID(self.clsid)

        # Create a new API from the specified path
        return self.helper.CreateObject(api_path)
