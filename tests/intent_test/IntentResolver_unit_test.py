from intent_handling import intent_resolver, tool_selector, tools
from src import service
from intent_handling.intent_resolver import IntentResolver
from intent_handling.cadocs_intents import CadocsIntents
from intent_handling.tool_selector import ToolSelector
from intent_handling.tools import CsDetectorTool
from unittest.mock import Mock
import pytest


class TestIntentResolverUT:

    @pytest.fixture
    def intent_resolver_instance(self):
        intent_resolver = IntentResolver()
        yield intent_resolver

    # Parametrization of tests with input for get smell and get smell date
    @pytest.mark.parametrize("intent, entities", [
        (CadocsIntents.GetSmells, ["https://github.com/tensorflow/ranking"]),
        (CadocsIntents.GetSmellsDate, [
         "https://github.com/tensorflow/ranking", "12/12/2022"]),
    ])
    def test_resolve_intent_get_smells_and_date(self, intent_resolver_instance, mocker, intent, entities):
        # Mock the run method of the ToolSelector class
        mocker.patch.object(ToolSelector, 'run', return_value="Test OK")

        result = intent_resolver_instance.resolve_intent(intent, entities)

        assert result == "Test OK"

    # Parametrization of tests with input for info and report
    @pytest.mark.parametrize("intent, entities", [
        (CadocsIntents.Info, []),
        (CadocsIntents.Report, []),
    ])
    def test_resolve_intent_info_and_report(self, intent_resolver_instance, mocker, intent, entities):
        result = intent_resolver_instance.resolve_intent(intent, entities)

        assert result == []
