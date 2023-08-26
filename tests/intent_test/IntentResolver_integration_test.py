from src.intent_handling import intent_resolver, tool_selector, tools
from src.intent_handling.intent_resolver import IntentResolver
from src.intent_handling.cadocs_intents import CadocsIntents
import pytest
import requests
import json
from tests import utils_tests


class TestIntentResolverIT:

    # The tests focus on the ability to resolve an intent and build the message

    # Creation of the instance of IntentResolver class
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
        # Mock the csDetector response
        response = {
            "files": [],
            "result": [
                "test",
                "response"
            ]
        }

        # Mock of the dotenv module
        mocker.patch('intent_handling.tools.os.environ.get',
                     return_value="CSDETECTOR_URL_GETSMELLS")

        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response
        mocker.patch("intent_handling.tools.requests.get", return_value=mock_response)

        result = intent_resolver_instance.resolve_intent(intent, entities)

        assert result == ["response"]

    # Parametrization of tests with input for info and report
    @pytest.mark.parametrize("intent, entities", [
        (CadocsIntents.Info, []),
        (CadocsIntents.Report, []),
    ])
    def test_resolve_intent_info_and_report(self, intent_resolver_instance, mocker, intent, entities):
        # Mock the csDetector response
        response = {
            "files": [],
            "result": [
                "test",
                "response"
            ]
        }

        # Mock of the dotenv module
        mocker.patch('intent_handling.tools.os.environ.get',
                     return_value="CSDETECTOR_URL_GETSMELLS")

        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response
        mocker.patch("intent_handling.tools.requests.get", return_value=mock_response)

        result = intent_resolver_instance.resolve_intent(intent, entities)

        assert result == []
