import pytest
import json
from src.service import cadocs_messages
from src.intent_handling.cadocs_intents import CadocsIntents
from tests import utils_tests

class TestCadocsMessagesUT:
    def test_build_cs_message_two_entities_zero_smell(self, mocker):
        smells_test=[]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "en")

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where zero smells are present is simulated

        utils_tests.append_final_block(blocks, "en")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response 

    def test_build_cs_message_two_entities_one_smell(self, mocker):
        smells_test=["OSE"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "en")

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where one smell (OSE) is present is simulated
        utils_tests.append_found_smells_block(smells_test, blocks, "en")

        utils_tests.append_final_block(blocks, "en")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_two_smells(self, mocker):
        smells_test=["OSE", "BCE"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")
        
        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "en")

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where two smells are present is simulated: OSE (Organizational Silo Effect) and BCE (Black-cloud Effect)
        utils_tests.append_found_smells_block(smells_test, blocks, "en")

        utils_tests.append_final_block(blocks, "en")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_one_smell_zero_strategies(self, mocker):
        smells_test=["SV"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")
        
        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "en")

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"
        
        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where one smell without strategies (SV) is present is simulated
        utils_tests.append_found_smells_block(smells_test, blocks, "en")

        utils_tests.append_final_block(blocks, "en")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response
    
    def test_build_cs_message_three_entities_two_smells(self, mocker):
        smells_test=["OSE", "BCE"]
        channel_test=1
        entities_test=["repository", "date", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "en")

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+" starting from "+entities_test[1]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where two smells are present is simulated: OSE (Organizational Silo Effect) and BCE (Black-cloud Effect)
        utils_tests.append_found_smells_block(smells_test, blocks, "en")

        utils_tests.append_final_block(blocks, "en")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_zero_smell_it(self, mocker):
        smells_test=[]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "it")

        text_test = "Questi sono i community smells che siamo stati in grado di rilevare nella repository "+entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where zero smells are present is simulated

        utils_tests.append_final_block(blocks, "it")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response 

    def test_build_cs_message_two_entities_one_smell_it(self, mocker):
        smells_test=["OSE"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "it")

        text_test = "Questi sono i community smells che siamo stati in grado di rilevare nella repository "+entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where one smell (OSE) is present is simulated
        utils_tests.append_found_smells_block(smells_test, blocks, "it")

        utils_tests.append_final_block(blocks, "it")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_two_smells_it(self, mocker):
        smells_test=["OSE", "BCE"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "it")

        text_test = "Questi sono i community smells che siamo stati in grado di rilevare nella repository "+entities_test[0]+":"

        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where two smells are present is simulated: OSE (Organizational Silo Effect) and BCE (Black-cloud Effect)
        utils_tests.append_found_smells_block(smells_test, blocks, "it")

        utils_tests.append_final_block(blocks, "it")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_one_smell_zero_strategies_it(self, mocker):
        smells_test=["SV"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "it")

        text_test = "Questi sono i community smells che siamo stati in grado di rilevare nella repository "+entities_test[0]+":"
        
        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where one smell without strategies (SV) is present is simulated
        utils_tests.append_found_smells_block(smells_test, blocks, "it")

        utils_tests.append_final_block(blocks, "it")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response
    
    def test_build_cs_message_three_entities_two_smells_it(self, mocker):
        smells_test=["OSE", "BCE"]
        channel_test=1
        entities_test=["repository", "date", "exec_type"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "it")

        text_test = "Questi sono i community smells che siamo stati in grado di rilevare nella repository "+entities_test[0]+" a partire da "+entities_test[1]+":"
        
        utils_tests.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where two smells are present is simulated: OSE (Organizational Silo Effect) and BCE (Black-cloud Effect)
        utils_tests.append_found_smells_block(smells_test, blocks, "it")

        utils_tests.append_final_block(blocks, "it")

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_report_message(self, mocker):
        channel_test=1
        exec_type_test="exec_type_test"
        results_test=["OSE", "BCE"]
        entities_test=["repository", "date"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")

        # The text block is created like in the function to test to later compare the results
        
        blocks = utils_tests.initial_block(user_test, "en")

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

        response = cadocs_messages.build_report_message(channel_test, exec_type_test, results_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response   

    def test_build_report_message_it(self, mocker):
        channel_test=1
        exec_type_test="exec_type_test"
        results_test=["OSE", "BCE"]
        entities_test=["repository", "date"]
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results
        
        blocks = utils_tests.initial_block(user_test, "it")

        blocks.append({
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Questo è una sintesi della sua ultima esecuzione",
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

        response = cadocs_messages.build_report_message(channel_test, exec_type_test, results_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response   

    def test_build_info_message(self, mocker):
        channel_test=1
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "en")

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

        response = cadocs_messages.build_info_message(channel_test, user_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_info_message_it(self, mocker):
        channel_test=1
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        # The text block is created like in the function to test to later compare the results

        blocks = utils_tests.initial_block(user_test, "it")

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

        response = cadocs_messages.build_info_message(channel_test, user_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_error_message(self, mocker):
        channel_test=1
        user_test="user_test"

        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="en")

        expected_response={
            "channel":channel_test,
            "blocks":[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hi "+user_test+", I'm sorry but I did not understand your intent. Please be more specific!"
                    }
                }
            ]
        }
        
        response = cadocs_messages.build_error_message(channel_test, user_test)
        # Assertions
        assert response == expected_response

    def test_build_error_message_it(self, mocker):
        channel_test=1
        user_test="user_test"
        
        # Mock the LanguageHandler.get_current_language method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.LanguageHandler.get_current_language', return_value="it")

        expected_response={
            "channel":channel_test,
            "blocks":[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Ciao "+user_test+", mi dispiace ma non sono riuscito a comprendere il suo intent. La prego di essere più specifico!"
                    }
                }
            ]
        }
        
        response = cadocs_messages.build_error_message(channel_test, user_test)
        # Assertions
        assert response == expected_response    

    def test_build_message_get_smells(self, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'src.service.cadocs_messages.build_cs_message', return_value="Test OK")
        
        result = cadocs_messages.build_message(
            "Test OK", user, "channel", CadocsIntents.GetSmells, ["https://github.com/tensorflow/ranking"])

        assert result == "Test OK"

    def test_build_message_get_smells_date(self, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch('src.service.cadocs_messages.build_cs_message', return_value="Test OK")
        result = cadocs_messages.build_message(
            "Test OK", user, "channel", CadocsIntents.GetSmellsDate, ["https://github.com/tensorflow/rankin, 12/12/2022"])

        assert result == "Test OK"

    def test_build_message_report(self, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'src.service.cadocs_messages.build_report_message', return_value="Test OK")
        result = cadocs_messages.build_message(
            "Test OK", user, "channel", CadocsIntents.Report, ["https://github.com/tensorflow/ranking", "12/12/2022", "report"])

        assert result == "Test OK"

    def test_build_message_info(self, mocker):
        user = {
            "profile": {
                "first_name": "test"
            }
        }

        # Mock the build_message method of the cadocs_messages module
        mocker.patch(
            'src.service.cadocs_messages.build_info_message', return_value="Test OK")
        result = cadocs_messages.build_message(
            "Test OK", user, "channel", CadocsIntents.Info, [])

        assert result == "Test OK"