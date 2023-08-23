from src import intent_resolver, service, tools, tool_selector
from intent_resolver import IntentResolver
from service.utils import CadocsIntents
from tool_selector import ToolSelector
from tools import CsDetectorTool
from tests.service_test.cadocs_messages_unit_test import TestCadocsMessagesUT
import pytest
import requests
import json


class TestIntentResolverIT:

    # The tests focus on the ability to resolve an intent and build the message

    # Creation of the instance of TestCadocsMessagesUT to use its methods to create text blocks
    @pytest.fixture
    def cadocs_messages_instance(self):
        test_cadocs_messages_ut_instance = TestCadocsMessagesUT()
        return test_cadocs_messages_ut_instance

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
        mocker.patch('tools.os.environ.get',
                     return_value="CSDETECTOR_URL_GETSMELLS")

        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response
        mocker.patch("tools.requests.get", return_value=mock_response)

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
        mocker.patch('tools.os.environ.get',
                     return_value="CSDETECTOR_URL_GETSMELLS")

        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response
        mocker.patch("tools.requests.get", return_value=mock_response)

        result = intent_resolver_instance.resolve_intent(intent, entities)

        assert result == []

    def test_build_message_get_smells(self, intent_resolver_instance, cadocs_messages_instance):
        user = {
            "profile": {
                "first_name": "test"
            }
        }
        intent_test = CadocsIntents.GetSmells
        smells_test = ["OSE", "BCE"]
        channel_test = 1
        entities_test = ["repository", "exec_type"]

        blocks = cadocs_messages_instance.initial_block(
            user.get("profile").get("first_name"))

        text_test = "These are the community smells we were able to detect in the repository " + \
            entities_test[0]+":"

        cadocs_messages_instance.append_second_block(
            blocks, text_test)

        cadocs_messages_instance.append_found_smells_block(smells_test, blocks)

        cadocs_messages_instance.append_final_block(blocks)

        result = intent_resolver_instance.build_message(
            smells_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response

    def test_build_message_report(self, intent_resolver_instance, cadocs_messages_instance):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        channel_test = 1
        exec_type_test = "exec_type_test"
        results_test = ["OSE", "BCE"]
        entities_test = ["repository", "date", "exec_type_test"]
        intent_test = CadocsIntents.Report

        blocks = cadocs_messages_instance.initial_block(
            user.get("profile").get("first_name"))

        blocks.append({
            "type": "section",
            "text": {
                    "type": "plain_text",
                    "text": "This is a summary of your last execution",
                    "emoji": True
            }
        })
        blocks.append({
            "type": "section",
            "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Type:*\n"+exec_type_test
                    },
                {
                        "type": "mrkdwn",
                        "text": "*Repository:*\n"+entities_test[0]
                }
            ]
        })
        smells = ""
        for r in results_test:
            smells = smells + r + "\n"
        blocks.append({
            "type": "section",
            "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Date:*\n"+entities_test[1]
                    },
                {
                        "type": "mrkdwn",
                        "text": "*Results:*\n"+smells
                }
            ]
        })

        result = intent_resolver_instance.build_message(
            results_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response

    def test_build_message_info(self, intent_resolver_instance, cadocs_messages_instance):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        channel_test = 1
        exec_type_test = "exec_type_test"
        results_test = ["OSE", "BCE"]
        entities_test = ["repository", "date", "exec_type_test"]
        intent_test = CadocsIntents.Info

        blocks = cadocs_messages_instance.initial_block(
            user.get("profile").get("first_name"))

        blocks.append({
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": "These are the *community smells* I can detect in your development communities:"
            }
        })
        blocks.append({
            "type": "divider"
        })

        with open('src/community_smells.json') as fp:
            data = json.load(fp)
            for i in data:
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*"+i.get('name')+"*  -  "+i.get('acronym')+"  -  "+i.get('emoji')+"\n"+i.get('description')
                        }
                    }
                )
        blocks.append({
            "type": "divider"
        })
        blocks.append({
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": "If you want to remain up-to-date, please follow us on our social networks:\n -Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab> \t -Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab> \t -Website: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io> \n Also, feel free to get in touch with us to have a discussion about the subject by sending us an email at slambiase@unisa.it!"
            }
        })

        result = intent_resolver_instance.build_message(
            results_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response
