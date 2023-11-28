from typing import Dict, List
import re
from slither.core.compilation_unit import SlitherCompilationUnit
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.slithir.operations import HighLevelCall
from slither.formatters.variables.unused_state_variables import custom_format
from slither.utils.output import Output

class EventSignatureMismatch(AbstractDetector):
    """
    Event Signature Mismatch Detector
    """

    ARGUMENT = "event-signature-mismatch"
    HELP = "Event Signature Mismatch"
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/crytic/slither"

    WIKI_TITLE = "Event Signature Mismatch"
    WIKI_DESCRIPTION = "Mismatch in event signature."
    WIKI_EXPLOIT_SCENARIO = "The emitted event does not match the expected signature."
    WIKI_RECOMMENDATION = "Ensure the event signature is consistent with expectations."

    def _detect(self)-> List[Output]:

        for contract in self.slither.contracts_derived:
            results = []
            true_count=0
            with open("C:\\Users\\Vatsal\\Desktop\\Iteration 3\\slither\\examples\\flat\\d.sol", "r") as file:
                solidity_code = file.read()

            def extract_function_statements(function_name, code):
                pattern = re.compile(r'\{([^}]+)\}')
                matches = pattern.findall(code)
                for match in matches:
                        pattern1 = re.compile(fr'{function_name}\((.*?)\)')
                        matche1 = pattern1.findall(match)
                        for mat in matche1:
                            parameters = mat.split(',')
                            values = [val.strip() for val in parameters]
                            return values   
                            #     return [param.strip() for param in parameters]
                            # return []
            expectparam = extract_function_statements("expectEmit", solidity_code)
            transferparam = extract_function_statements("Transfer", solidity_code)


            for para in expectparam:
                if para=='true':
                    true_count+=1
            
            if len(transferparam)!=true_count:
                info="Arguments of expectEmit() and Transfer() do not match\n"
                json=self.generate_result(info)
                results.append(json)

        ck = True
        for event in contract.events_declared:
            if(event.name)=="Transfer":
                for i in range(len(transferparam)):
                    if i!=len(transferparam)-1:
                        if not event.elems[i].indexed:
                            ck=False
                            info = f"Vulnerability Found in {contract.name} for {event.elems[i]} as indexed address was expected and {event.elems[i].type} was found.\n"
                            json = self.generate_result(info)
                            results.append(json)
                    else:
                        if event.elems[len(transferparam)-1].type != 'uint':
                            ck = False
                            info = f"Vulnerability Found in {contract.name} for {event.elems[i]} as a uint was expected, but {event.elems[i].type} was found.\n"
                            json = self.generate_result(info)
                            results.append(json)
        return results
                 
            
            # if ck==False: 
            #     info = "Event Signature Mismatch Found.\n"
            #     json = self.generate_result(info)
            #     results.append(json)
def make_plugin():
    return EventSignatureMismatch
