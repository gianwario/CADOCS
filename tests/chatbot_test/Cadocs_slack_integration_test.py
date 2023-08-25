from intent_handling import intent_resolver
from src import service, chatbot
from chatbot.intent_manager import IntentManager
from intent_handling.intent_resolver import IntentResolver
from intent_handling.cadocs_intents import CadocsIntents
from chatbot.cadocs_slack import CadocsSlack
from tests.service_test.cadocs_messages_unit_test import TestCadocsMessagesUT
import requests
from unittest.mock import Mock, patch
import pytest
import json


class TestCadocsSlackIT:

    @pytest.fixture
    def cadocs_instance(self):
        cadocs = CadocsSlack()
        yield cadocs

    def test_new_message_get_smells_valid_link(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking",
            "approved": True,
            "executed": False
        }
        user = {
            "id": "1",
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        response_intent_manager = {
            "intent": {
                "intent": {
                    "name": "get_smells",
                    "confidence": 0.8
                }
            },
            "entities": {"url": "https://github.com/tensorflow/ranking"}
        }

        response = {
            "files": [],
            "result": [
                "test",
                "BCE"
            ]
        }

        # Mock the Response objects with a mock dict
        mock_response_intent_manager = Mock(spec=requests.Response)
        mock_response_intent_manager.json.return_value = response_intent_manager
        mock_response_tools = Mock(spec=requests.Response)
        mock_response_tools.json.return_value = response

        # Mock requests.get method
        mocker.patch("chatbot.intent_manager.requests.get",
                     side_effect=[mock_response_intent_manager, mock_response_tools])

        # Mock os.environ.get method
        mocker.patch('intent_handling.tools.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.77", "0.55", "0.77"])

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        # The produced message is not asserted in this class because it was already tested in unit test
        assert results == ["BCE"]
        assert entities == ["https://github.com/tensorflow/ranking", "1"]
        assert intent == CadocsIntents.GetSmells

    def test_new_message_get_smells_valid_date(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking from 10/10/2020",
            "approved": True,
            "executed": False
        }
        user = {
            "id": "1",
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        response_intent_manager = {
            "intent": {
                "intent": {
                    "name": "get_smells_date",
                    "confidence": 0.8
                }
            },
            "entities": {"url": "https://github.com/tensorflow/ranking",
                         "date": "10/10/2020"}
        }

        response = {
            "files": [],
            "result": [
                "test",
                "BCE"
            ]
        }

        # Mock the Response objects with a mock dict
        mock_response_intent_manager = Mock(spec=requests.Response)
        mock_response_intent_manager.json.return_value = response_intent_manager
        mock_response_tools = Mock(spec=requests.Response)
        mock_response_tools.json.return_value = response

        # Mock requests.get method
        mocker.patch("chatbot.intent_manager.requests.get",
                     side_effect=[mock_response_intent_manager, mock_response_tools])

        # Mock os.environ.get method
        mocker.patch('intent_handling.tools.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.77", "0.55", "0.77"])

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert results == ["BCE"]
        assert entities == [
            "https://github.com/tensorflow/ranking", "10/10/2020", "1"]
        assert intent == CadocsIntents.GetSmellsDate

    def test_new_message_get_smells_valid_link_low_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking",
            "approved": False,
            "executed": False
        }
        user = {
            "id": "1",
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        response_intent_manager = {
            "intent": {
                "intent": {
                    "name": "get_smells",
                    "confidence": 0.2
                }
            },
            "entities": {"url": "https://github.com/tensorflow/ranking"}
        }

        # Mock the Response objects with a mock dict
        mock_response_intent_manager = Mock(spec=requests.Response)
        mock_response_intent_manager.json.return_value = response_intent_manager

        # Mock requests.get method
        mocker.patch("chatbot.intent_manager.requests.get",
                     return_value=mock_response_intent_manager)

        # Mock os.environ.get method
        mocker.patch('os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.77", "0.55", "0.77", "0.5"])

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_w_ask_confirm(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking",
            "approved": False,
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        channel_test = 1
        response_intent_manager = {
            "intent": {
                "intent": {
                    "name": "get_smells",
                    "confidence": 0.6
                }
            },
            "entities": {"url": "https://github.com/tensorflow/ranking"}
        }

        mocker.patch('intent_handling.tools.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.77", "0.55"])
        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response_intent_manager
        mocker.patch("chatbot.intent_manager.requests.get", return_value=mock_response)

        response = {
            "files": [],
            "result": [
                "test",
                "response"
            ]
        }

        expected_response = {
            "channel": 1,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Do you want me to predict community smells?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Yes",
                                "emoji": True
                            },
                            "value": "yes",
                            "action_id": "action-yes"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "No",
                                "emoji": True
                            },
                            "value": "no",
                            "action_id": "action-no"
                        }
                    ]
                }
            ]
        }

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, channel_test, user)

        # Assertions
        assert response == expected_response
        assert results == None
        assert entities == None
        assert intent == None
