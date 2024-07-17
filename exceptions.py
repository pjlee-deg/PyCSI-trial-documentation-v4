"""PyCSI custom exceptions classes

The following exceptions are used to indicate errors and warnings raised while 
connecting or requesting data to the CSI API
"""


class APIBadRequest(Exception):
    """API Request Error

    This exception is raised when the request to the CSI API does not return 
    any data.

    Arguments:
        message -- Error message
        error_code -- The integer error code from the CSI API request

    Raises:
        Exception APIBadRequest

    Example:
        .. codeblock:: python

            from pyCSI import ETABSModel
            from pyCSI import APIBadRequest

            # Connect to a model
            model = ETABSModel()
            model.get_model()

            # Request for a non-existing table
            try:
                model.tables.get_table_dataframe(table="Generic Table")

            except APIBadRequest as e:
                print(f'Error: {e.message}, Error Code: {e.error_code}')
    """

    def __init__(self, message: str, error_code: int) -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class APIConnectionError(Exception):
    """API Connection Error.

    This exception is raised when an error occurs while connecting to a model.

    Arguments:
        message -- Error message

    Raises:
        Exception APIConnectionError

    Example:
        .. codeblock:: python

            from pyCSI import ETABSModel
            from pyCSI import APIConnectionError

            # Trying to connect to an ETABS active window while the 
            # program is closed
            model = ETABSModel()
            try:
                model.get_model()

            except APIConnectionError as e:
                print(f'Error: {e.message}')
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
