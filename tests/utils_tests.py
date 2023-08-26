import json

# Functions to create and modify text blocks are defined here
def initial_block(user_test):
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

def append_second_block(blocks, text_test):
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

def append_found_smells_block(smells_test, blocks):
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

def append_final_block(blocks):
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
