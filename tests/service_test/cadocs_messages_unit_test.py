import pytest
import json
from src.service import cadocs_messages

class TestCadocsMessagesUT:

    # Functions to create and modify text blocks are defined here

    def initial_block(self, user_test):
        blocks = []
        blocks.append(
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Hi "+user_test+" :wave:",
                        "emoji": True
                    }
                }
        )
        
        return blocks   
    
    def append_second_block(self, blocks, text_test):
        blocks.append(
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": text_test,
                "emoji": True
            }
        }
        )

    def append_found_smells_block(self, smells_test, blocks):
        with open('src/community_smells.json') as fp:
            data = json.load(fp)
            for s in smells_test:
                smell_data = [sm for sm in data if sm["acronym"] == s]
                
                blocks.append({
                        "type": "divider"
                    })
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":"*"+ s +"* "+ smell_data[0].get("name") +" "+smell_data[0].get("emoji") +"\n_"+smell_data[0].get("description")+"_"
                        }
                    }
                )
                strategies = smell_data[0].get("strategies")

                if(len(strategies) > 0):
                    blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Some possible mitigation strategies are:"
                        }
                    })
                    for st in strategies:
                            blocks.append({
                                "type": "section",
                                "fields": [{
                                    "type": "mrkdwn",
                                    "text": ">"+st.get("strategy")+"" 
                                }, {
                                    "type": "mrkdwn",
                                    "text": st.get("stars"),
                                }
                            ]})

    def append_final_block(self, blocks):
        blocks.append({
                    "type": "divider"
                })
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "See you soon :wave:"
                }
            } 
        )
    
    def test_build_cs_message_two_entities_zero_smell(self):
        smells_test=[]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results

        blocks = self.initial_block(user_test)

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"

        self.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where zero smells are present is simulated

        self.append_final_block(blocks)

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response 

    def test_build_cs_message_two_entities_one_smell(self):
        smells_test=["OSE"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results

        blocks = self.initial_block(user_test)

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"

        self.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where one smell (OSE) is present is simulated
        self.append_found_smells_block(smells_test, blocks)

        self.append_final_block(blocks)

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_two_smells(self):
        smells_test=["OSE", "BCE"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results

        blocks = self.initial_block(user_test)

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"

        self.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where two smells are present is simulated: OSE (Organizational Silo Effect) and BCE (Black-cloud Effect)
        self.append_found_smells_block(smells_test, blocks)

        self.append_final_block(blocks)

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_cs_message_two_entities_one_smell_zero_strategies(self):
        smells_test=["SV"]
        channel_test=1
        entities_test=["repository", "exec_type"]
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results

        blocks = self.initial_block(user_test)

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+":"
        
        self.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where one smell without strategies (SV) is present is simulated
        self.append_found_smells_block(smells_test, blocks)

        self.append_final_block(blocks)

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response
    
    def test_build_cs_message_three_entities_two_smells(self):
        smells_test=["OSE", "BCE"]
        channel_test=1
        entities_test=["repository", "date", "exec_type"]
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results

        blocks = self.initial_block(user_test)

        text_test = "These are the community smells we were able to detect in the repository "+entities_test[0]+" starting from "+entities_test[1]+":"

        self.append_second_block(blocks, text_test)

        # It was decided not to mock the open function for files

        # The case where two smells are present is simulated: OSE (Organizational Silo Effect) and BCE (Black-cloud Effect)
        self.append_found_smells_block(smells_test, blocks)

        self.append_final_block(blocks)

        response = cadocs_messages.build_cs_message(smells_test, channel_test, user_test, entities_test)

        expected_response = {"channel" : channel_test,
                             "blocks": blocks}
        
        # Assertions
        assert response == expected_response

    def test_build_report_message(self):
        channel_test=1
        exec_type_test="exec_type_test"
        results_test=["OSE", "BCE"]
        entities_test=["repository", "date"]
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results
        
        blocks = self.initial_block(user_test)

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

    def test_build_info_message(self):
        channel_test=1
        user_test="user_test"

        # The text block is created like in the function to test to later compare the results

        blocks = self.initial_block(user_test)

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

    def test_build_error_message(self):
        channel_test=1
        user_test="user_test"
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