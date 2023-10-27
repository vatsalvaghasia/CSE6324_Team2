"""
Module detecting unused state variables
"""
from typing import List, Optional, Dict

from slither.core.compilation_unit import SlitherCompilationUnit
from slither.core.declarations import Function
from slither.core.declarations.contract import Contract
from slither.core.solidity_types import ArrayType
from slither.core.variables import Variable
from slither.core.variables.state_variable import StateVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.formatters.variables.unused_state_variables import custom_format
from slither.utils.output import Output
from slither.visitors.expression.export_values import ExportValues


# from slither.core.variable import StateVariable

def detect_unused_constants(contract: Contract) -> Optional[List[StateVariable]]:
    # Get all the state variables declared in the contract
    all_state_variables = contract.state_variables

    # Get all the functions and modifiers in the contract
    all_functions = [
        f
        for f in contract.all_functions_called + list(contract.modifiers)
        if isinstance(f, Function)
    ]

    # Get all state variables read and written in the functions and modifiers
    state_variables_read = [x.state_variables_read for x in all_functions]
    state_variables_written = [
        x.state_variables_written for x in all_functions if not x.is_constructor_variables
    ]

    # Flatten the lists of state variables
    state_variables_read = [item for sublist in state_variables_read for item in sublist]
    state_variables_written = [item for sublist in state_variables_written for item in sublist]

    # Combine all accessed state variables
    accessed_state_variables = state_variables_read + state_variables_written

    # Identify constant state variables that are not accessed
    unused_constants = [
        state_var
        for state_var in all_state_variables
        if state_var.is_constant and state_var.visibility != "public" and state_var not in accessed_state_variables
    ]

    return unused_constants




class UnusedConstants(AbstractDetector):
    """
    Unused state variables detector
    """

    ARGUMENT = "unused-constant"
    HELP = "Unused Constants"
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/crytic/slither/wiki/Detector-Documentation#unused-constant"

    WIKI_TITLE = "Unused state variable"
    WIKI_DESCRIPTION = "Unused state variable."
    WIKI_EXPLOIT_SCENARIO = ""
    WIKI_RECOMMENDATION = "Remove unused state variables."

    def _detect(self) -> List[Output]:
        """Detect unused state variables"""
        results = []
        for c in self.compilation_unit.contracts_derived:
            if c.is_signature_only():
                continue
            unusedVars = detect_unused_constants(c)
            if unusedVars:
                for var in unusedVars:
                    info: DETECTOR_INFO = [var, " is never used.\n"]
                    json = self.generate_result(info)
                    results.append(json)

        return results

    @staticmethod
    def _format(compilation_unit: SlitherCompilationUnit, result: Dict) -> None:
        custom_format(compilation_unit, result)
