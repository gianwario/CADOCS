from utils import CadocsIntents
from tool_selector import ToolSelector
from tools import CsDetectorTool
import cadocs_messages

# the Intent Resolver is used to handle the execution given a predicted intent
class IntentResolver:
    def resolve_intent(self, intent, entities):
        #check if the intent is a Cadocs intent (looking forward to have multiple tools)
        if intent in CadocsIntents:
            # we instantiate our strategy context
            tool = ToolSelector(CsDetectorTool())
            # then we execute the selected tool with given entities
            results = tool.run(entities)
            return results
        # else if intent in OtherToolIntent

    # this function will format the message basing on the intent
    def build_message(self, results, username, channel, intent, entities):
        if(intent == CadocsIntents.GetSmells):
            response = cadocs_messages.get_cs_message(results, channel, username, entities[0])
            return response
            

