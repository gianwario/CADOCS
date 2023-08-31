import json

# Functions to create and modify text blocks are defined here
def initial_block(user_test, lang):
    blocks = []
    if lang == "en":
        text = "Hi " + user_test + " :wave:"
    elif lang == "it":
        text = "Ciao " + user_test + " :wave:"
    blocks.append(
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": text,
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

def append_found_smells_block(smells_test, blocks, lang):
    if lang == "en":
        fileName = 'src/community_smells.json'
    elif lang == "it":
        fileName = 'src/community_smells_it.json'

    with open(fileName) as fp:
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
                if lang == "en":
                    text = "Some possible mitigation strategies are:"
                elif lang == "it":
                    text = "Alcuni possibili strategie per la mitigazione sono:"
                blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
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

def append_final_block(blocks, lang):
    blocks.append({
                "type": "divider"
            })
    if lang == "en":
        text = "See you soon :wave:"
    elif lang == "it":
        text = "A presto :wave:"
    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        } 
    )
