from service.utils import CadocsIntents
from tool_selector import ToolSelector
from tools import CsDetectorTool
from service import cadocs_messages

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

    # this function will format the message basing on the intent
    def build_message(self, results, user, channel, intent, entities):
        username = user.get('profile').get('first_name')
        if intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
            response = cadocs_messages.build_cs_message(
                results, channel, username, entities)
            return response
        elif intent == CadocsIntents.Report:
            response = cadocs_messages.build_report_message(
                channel, entities[2], results, username, entities)
            return response
        elif intent == CadocsIntents.Info:
            response = cadocs_messages.build_info_message(channel, username)
            return response
