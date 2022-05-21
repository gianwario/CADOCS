from utils import CadocsIntents
from tool_selector import Tools, ToolSelector
class IntentResolver:
    def resolve_intent(self, intent, entities):
        tool = ToolSelector()
        #check if the intent is a Cadocs intent (looking forward to have multiple tools)
        if intent in CadocsIntents:
            # then we execute the selected tool with given entities
            results = tool.execute_tool(Tools.CsDetector, entities)
            return results
        # else if intent in OtherToolIntent

        

