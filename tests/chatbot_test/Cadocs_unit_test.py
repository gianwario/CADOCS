from src import intent_manager, intent_resolver, utils, cadocs
from intent_manager import IntentManager
from intent_resolver import IntentResolver
from utils import CadocsIntents
from cadocs import Cadocs
import pytest


class TestCadocsUT:

    @pytest.fixture
    def cadocs_instance(self):
        cadocs = Cadocs()
        yield cadocs

    def test_new_message_get_smells_valid_link_high_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https-://github.com/tensorflow/ranking",
            "approved": True,
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https://github.com/tensorflow/ranking"]
        mocked_confidence = 0.8

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the IntentResolver object
        mocked_results = "Test OK"
        mocker.patch.object(IntentResolver, 'resolve_intent',
                            return_value=(mocked_results))

        # Mock the build_message method
        mocker.patch.object(IntentResolver, 'build_message',
                            return_value="get smells")

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == "get smells"
        assert results == "Test OK"
        assert entities == ["https://github.com/tensorflow/ranking", 1]
        assert intent == CadocsIntents.GetSmells

    def test_new_message_get_smells_valid_link_medium_confidence(self, cadocs_instance, mocker):
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

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https://github.com/tensorflow/ranking"]
        mocked_confidence = 0.6

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the ask_confirm method
        mocked_result = "Confirm message"
        mocker.patch.object(Cadocs, 'ask_confirm',
                            return_value=(mocked_result))

        # Mock the build_message method
        mocker.patch.object(IntentResolver, 'build_message',
                            return_value="get smells")

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_result
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_valid_link_low_confidence(self, cadocs_instance, mocker):
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

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https://github.com/tensorflow/ranking"]
        mocked_confidence = 0.2

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the build_error_message method
        mocked_result = "Error message"
        mocker.patch('cadocs.build_error_message',
                     return_value=mocked_result)

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_result
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_not_valid_link(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking",
            "approved": True,
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https:github.comtensorflowranking"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=False)

        # Mock error_message method
        msg = "Error: Invalid link"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)
        # Assertions
        assert response == "Error: Invalid link"

    def test_new_message_get_smells_date_valid_link_valid_date_high_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking from 12/12/2022",
            "approved": True,
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = [
            "https://github.com/tensorflow/ranking", "12/12/2022"]
        mocked_confidence = 0.8

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('cadocs.valid_date', return_value=True)

        # Mock the IntentResolver object
        mocked_results = "Test OK"
        mocker.patch.object(IntentResolver, 'resolve_intent',
                            return_value=(mocked_results))

        # Mock the build_message method
        mocker.patch.object(IntentResolver, 'build_message',
                            return_value="get smells date")

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == "get smells date"
        assert results == "Test OK"
        assert entities == [
            "https://github.com/tensorflow/ranking", "12/12/2022", 1]
        assert intent == CadocsIntents.GetSmellsDate

    def test_new_message_get_smells_date_valid_link_valid_date_medium_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking from 12/12/2022",
            "approved": False,
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = [
            "https://github.com/tensorflow/ranking", "12/12/2022"]
        mocked_confidence = 0.6

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('cadocs.valid_date', return_value=True)

        # Mock the ask_confirm method
        mocked_result = "Confirm message"
        mocker.patch.object(Cadocs, 'ask_confirm',
                            return_value=(mocked_result))

        # Mock the build_message method
        mocker.patch.object(IntentResolver, 'build_message',
                            return_value="get smells")

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_result
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_date_valid_link_valid_date_low_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking from 12/12/2022",
            "approved": False,
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = [
            "https://github.com/tensorflow/ranking", "12/12/2022"]
        mocked_confidence = 0.2

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('cadocs.valid_date', return_value=True)

        # Mock the build_error_message method
        mocked_result = "Error message"
        mocker.patch('cadocs.build_error_message',
                     return_value=mocked_result)

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_result
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_date_not_valid_link(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking from 12/12/2022",
            "approved": True,
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = ["https:github.comtensorflowranking", "12/12/2022"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=False)

        # Mock the valid_date method
        mocker.patch('cadocs.valid_date', return_value=True)

        # Mock error_message method
        msg = "Error: Invalid link"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)

        # Assertions
        assert response == "Error: Invalid link"

    def test_new_message_get_smells_date_not_valid_date(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking from 1212/2022",
            "approved": True,
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = ["https://github.comtensorflowranking", "1212/2022"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('cadocs.valid_date', return_value=False)

        # Mock error_message method
        msg = "Error: Invalid date"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)

        # Assertions
        assert response == "Error: Invalid date"

    def test_new_message_get_smells_date_not_valid_link_not_valid_date(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking from 12/12/2022",
            "approved": True,
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = ["https:github.comtensorflowranking", "12/12/2022"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('cadocs.valid_link', return_value=False)

        # Mock the valid_date method
        mocker.patch('cadocs.valid_date', return_value=False)

        # Mock error_message method
        msg = "Error: Invalid link and date"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)

        # Assertions
        assert response == "Error: Invalid link and date"

    def test_new_message_report(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you give me your last report",
            "approved": True,
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.Report
        mocked_entities = []
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the IntentResolver object
        mocked_results = "Test OK"
        mocker.patch.object(IntentResolver, 'resolve_intent',
                            return_value=(mocked_results))

        # Mock get_last_execution method
        mocked_last_ex = {"results": "Test OK", "repo": "https://github.com/tensorflow/ranking",
                          "date": "12/12/2022", "exec_type": "get_smells"}
        mocker.patch.object(
            cadocs_instance, 'get_last_execution', return_value=mocked_last_ex)

        # Mock build_message method
        mocked_response = "Report message"
        mocker.patch.object(IntentResolver, 'build_message',
                            return_value=mocked_response)

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_response
        assert results == "Test OK"
        assert entities == [
            "https://github.com/tensorflow/ranking", "12/12/2022", "get_smells"]
        assert intent == CadocsIntents.Report

    @pytest.mark.parametrize("intent, text", [
        (CadocsIntents.GetSmells, "Do you want me to predict community smells?"),
        (CadocsIntents.GetSmellsDate,
         "Do you want me to predict community smells starting from a specific date?"),
        (CadocsIntents.Report, "Do you want me to show a report of your last execution?"),
        (CadocsIntents.Info, "Do you want to know more about community smells?"),
    ])
    def test_ask_confirm_get_smell(self, cadocs_instance, intent, text):
        user = "user"
        channel = "channel"

        msg = {
            "channel": channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
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

        response = cadocs_instance.ask_confirm(intent, channel, user)

        assert response == msg

    def test_get_last_execution_missing_file(self, cadocs_instance, mocker):
        user_test = "user"
        # Mock the path.isfile method
        mocker.patch('cadocs.path.isfile', return_value=False)

        # Assertions
        with pytest.raises(Exception, match="File not found"):
            cadocs_instance.get_last_execution(user_test)

    def test_error_message_url(self, cadocs_instance):
        error_type = "url"
        username_test = "user_test"
        channel_test = 1
        txt = "Hi "+username_test+", there was an error processing your request. \n You provided an invalid repository link. Check the availability of the link on GitHub."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None

    def test_error_message_date(self, cadocs_instance):
        error_type = "date"
        username_test = "user_test"
        channel_test = 1
        txt = "Hi "+username_test+", there was an error processing your request. \n You provided an invalid starting date. Remember that the correct format is MM/DD/YYYY."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None

    def test_error_message_date_url(self, cadocs_instance):
        error_type = "date_url"
        username_test = "user_test"
        channel_test = 1
        txt = "Hi "+username_test + \
            ", there was an error processing your request. \n You provided an invalid repository link and an invalid starting date. Check both the availability of the link on GitHub and the format of the date (MM/DD/YYYY)."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None

    def test_something_wrong(self, cadocs_instance):
        channel_test = 1
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Something went wrong with your request. Please try again",
                "emoji": True
            }
        }]}
        response = cadocs_instance.something_wrong(channel_test)

        # Assertions
        assert response == expected_response
