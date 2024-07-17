"""
=====
PyCSI Analysis component
=====

The Analysis component gives access to the model CSI API Analyze Interface
"""

from typing import Optional

from pyCSI.protocols import IAnalysis
from pyCSI.utils import check_request


class Analysis:
    """Analysis interface of the Model object.

    Args:
        parent (Model): Instance of a PyCSI Model class.
    """

    def __init__(self, parent) -> None:
        self._parent = parent
        self._analyze: IAnalysis = parent.get_model_object().Analyze

    def run_analysis(self) -> None:
        """Runs the analysis for the model object"""

        print('Running analysis...')
        return_code = self._analyze.RunAnalysis()
        check_request(return_code)
        print('Analysis finished!')

    def set_load_cases_to_run(self, run: bool, load_cases: Optional[list[str]] = None):
        """Set the specified load cases to be run.

        Args:
            run: If `True`, set the specified load cases to be Run, otherwise set 
            to Not Run.

            load_cases: List of load cases to be set. If not provided run flag 
            will be set for all load cases defined in the model. Defaults to
            None.
        """
        # Set run flag for all available load cases
        if load_cases is None:
            return_code = self._analyze.SetRunCaseFlag('', run, True)
            check_request(return_code)
            return

        # Set run flag for specific load cases
        for case in load_cases:
            return_code = self._analyze.SetRunCaseFlag(case, run)
            check_request(return_code)

    def delete_results(self, load_cases: Optional[list[str]] = None):
        """Deletes the results for the specified load cases.

        Args:
            load_cases: List of load cases which results will be deleted. 
            If not provided, results will be deleted for all load cases
            defined in the model. Defaults to None.
        """
        # Delete results for all available load cases
        if load_cases is None:
            return_code = self._analyze.DeleteResults('', all=True)
            check_request(return_code)
            return

        # Delete results for specific load cases
        for case in load_cases:
            return_code = self._analyze.DeleteResults(case)
            check_request(return_code)
