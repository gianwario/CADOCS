from intent_handling.cadocs_intents import CadocsIntents
from intent_handling.tool_selector import ToolSelector
from intent_handling.tools import CsDetectorTool

# the Intent Resolver is used to handle the execution given a predicted intent
class IntentResolver:
    def resolve_intent(self, intent, entities):
        # check if the intent is a Cadocs intent (looking forward to have multiple tools)
        if intent in CadocsIntents:
            # execute csdetector and build smell detection message
            if intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
                # we instantiate our strategy context
                tool = ToolSelector(CsDetectorTool())
                # then we execute the selected tool with given entities
                results = tool.run(entities)
                return results
            # build info message
            elif intent == CadocsIntents.Info:
                return []
            # build report message
            elif intent == CadocsIntents.Report:
                return []

        # else if intent in OtherToolIntent
