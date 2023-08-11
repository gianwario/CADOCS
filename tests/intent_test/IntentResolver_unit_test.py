from src import intent_resolver, utils, tools, tool_selector
from intent_resolver import IntentResolver
from utils import CadocsIntents
from tool_selector import ToolSelector
from tools import CsDetectorTool
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

    def test_build_message_get_smells(self, intent_resolver_instance, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'intent_resolver.cadocs_messages.build_cs_message', return_value="Test OK")
        result = intent_resolver_instance.build_message(
            "Test OK", user, "channel", CadocsIntents.GetSmells, ["https://github.com/tensorflow/ranking"])

        assert result == "Test OK"

    def test_build_message_get_smells_date(self, intent_resolver_instance, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'intent_resolver.cadocs_messages.build_cs_message', return_value="Test OK")
        result = intent_resolver_instance.build_message(
            "Test OK", user, "channel", CadocsIntents.GetSmellsDate, ["https://github.com/tensorflow/rankin, 12/12/2022"])

        assert result == "Test OK"

    def test_build_message_report(self, intent_resolver_instance, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'intent_resolver.cadocs_messages.build_report_message', return_value="Test OK")
        result = intent_resolver_instance.build_message(
            "Test OK", user, "channel", CadocsIntents.Report, ["https://github.com/tensorflow/ranking", "12/12/2022", "report"])

        assert result == "Test OK"

    def test_build_message_info(self, intent_resolver_instance, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'intent_resolver.cadocs_messages.build_info_message', return_value="Test OK")
        result = intent_resolver_instance.build_message(
            "Test OK", user, "channel", CadocsIntents.Info, [])

        assert result == "Test OK"
