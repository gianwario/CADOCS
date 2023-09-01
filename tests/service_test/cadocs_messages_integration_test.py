from src.intent_handling import intent_resolver, tool_selector, tools
from src.intent_handling.cadocs_intents import CadocsIntents
from src.service import cadocs_messages
import pytest
import json
from tests import utils_tests
from src.service.language_handler import LanguageHandler

class TestCadocsMessagesIT:

    # This variable is used to set the current language for each test method
    language_handler = LanguageHandler()
    
    def test_build_message_get_smells(self):
        user = {
            "profile": {
                "first_name": "test"
            }
        }
        intent_test = CadocsIntents.GetSmells
        smells_test = ["OSE", "BCE"]
        channel_test = 1
        entities_test = ["repository", "exec_type"]
        
        self.language_handler.detect_language("Text in English")

        blocks = utils_tests.initial_block(user.get("profile").get("first_name"), "en")

        text_test = "These are the community smells we were able to detect in the repository " + \
            entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        utils_tests.append_found_smells_block(smells_test, blocks, "en")

        utils_tests.append_final_block(blocks, "en")

        result = cadocs_messages.build_message(
            smells_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response

    def test_build_message_get_smells_it(self):
        user = {
            "profile": {
                "first_name": "test"
            }
        }
        intent_test = CadocsIntents.GetSmells
        smells_test = ["OSE", "BCE"]
        channel_test = 1
        entities_test = ["repository", "exec_type"]
        
        self.language_handler.detect_language("Testo in Italiano")

        blocks = utils_tests.initial_block(user.get("profile").get("first_name"), "it")

        text_test = "Questi sono i community smells che siamo stati in grado di rilevare nella repository " + \
            entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        utils_tests.append_found_smells_block(smells_test, blocks, "it")

        utils_tests.append_final_block(blocks, "it")

        result = cadocs_messages.build_message(
            smells_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response
    
    def test_build_message_report(self):
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

        self.language_handler.detect_language("Text in English")
        blocks = utils_tests.initial_block(user.get("profile").get("first_name"), "en")

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

        result = cadocs_messages.build_message(
            results_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response

    def test_build_message_report_it(self):
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

        self.language_handler.detect_language("Testo in Italiano")

        blocks = utils_tests.initial_block(user.get("profile").get("first_name"), "it")

        blocks.append({
            "type": "section",
            "text": {
                    "type": "plain_text",
                    "text": "Questo è una sintesi della tua ultima esecuzione",
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

        result = cadocs_messages.build_message(
            results_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response    

    def test_build_message_info(self):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        self.language_handler.detect_language("Text in English")

        channel_test = 1
        exec_type_test = "exec_type_test"
        results_test = ["OSE", "BCE"]
        entities_test = ["repository", "date", "exec_type_test"]
        intent_test = CadocsIntents.Info

        blocks = utils_tests.initial_block(
            user.get("profile").get("first_name"), "en")

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

        result = cadocs_messages.build_message(
            results_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response

    def test_build_message_info(self):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        self.language_handler.detect_language("Testo in Italiano")

        channel_test = 1
        exec_type_test = "exec_type_test"
        results_test = ["OSE", "BCE"]
        entities_test = ["repository", "date", "exec_type_test"]
        intent_test = CadocsIntents.Info

        blocks = utils_tests.initial_block(user.get("profile").get("first_name"), "it")

        blocks.append({
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": "Questi sono i *community smells* che riesco a individuare nelle vostre community:"
            }
        })
        blocks.append({
            "type": "divider"
        })

        with open('src/community_smells_it.json') as fp:
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
                    "text": "Se volete rimanere aggiornati, seguite i canali social:\n -Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab> \t -Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab> \t -Sito web: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io> \n Inoltre, sentitevi liberi di mettervi in contatto con noi per discutere dell'argomento inviandoci una mail a slambiase@unisa.it!"
            }
        })

        result = cadocs_messages.build_message(
            results_test, user, channel_test, intent_test, entities_test)

        expected_response = {"channel": channel_test,
                             "blocks": blocks}

        # Assertion
        assert result == expected_response