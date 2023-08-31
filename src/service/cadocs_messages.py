import json
from src.intent_handling.cadocs_intents import CadocsIntents
from service.language_handler import LanguageHandler

# building of the message for the intent GetCommunitySmells or GetCommunitySmellsDate
def build_cs_message(smells, channel, user, entities):
    lang = LanguageHandler().get_current_language()

    print(smells, entities)
    # blocks that will be displayed in slack
    blocks = []
    if lang == "en":
        text = "Hi " + user + " :wave:"
    elif lang == "it":
        text = "Ciao " + user + " :wave:"

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
    if len(entities) > 2:
        if lang == "en":
            text = "These are the community smells we were able to detect in the repository " + entities[0] + " starting from " + entities[1] + ":"
        elif lang == "it":
            text = "Questi sono i community smells che siamo stati in grado di rilevare nella repository " + entities[0] + " a partire da " + entities[1] + ":"
    else:
        if lang == "en":
            text = "These are the community smells we were able to detect in the repository " + entities[0] + ":"
        elif lang == "it":
            text = "Questi sono i community smells che siamo stati in grado di rilevare nella repository " + entities[0] + ":"
    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True
            }
        }
    )
    # appending blocks for each smell detected
    if lang == "en":
        fileName = 'src/community_smells.json'
    elif lang == "it":
        fileName = 'src/community_smells_it.json'
    with open(fileName) as fp:
        data = json.load(fp)
        for s in smells:
            smell_data = [sm for sm in data if sm["acronym"] == s]

            blocks.append({
                "type": "divider"
            })
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*" + s + "* " + smell_data[0].get("name") + " "+smell_data[0].get("emoji") + "\n_"+smell_data[0].get("description")+"_"
                    }
                }
            )
            strategies = smell_data[0].get("strategies")

            # appending strategies if existing
            if (len(strategies) > 0):
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

    return {
        "channel": channel,
        "blocks": blocks
    }

# building the message for the Report intent
def build_report_message(channel, exec_type, results, user, entities):
    lang = LanguageHandler().get_current_language()
    
    # blocks that will be displayed in slack
    blocks = []
    if lang == "en":
        text = "Hi " + user + " :wave:"
    elif lang == "it":
        text = "Ciao " + user + " :wave:"
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
    if lang == "en":
        text = "This is a summary of your last execution"
    elif lang == "it":
        text = "Questo è una sintesi della tua ultima esecuzione"
    blocks.append({
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True
        }
    })
    blocks.append({
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*Type:*\n"+exec_type
            },
            {
                "type": "mrkdwn",
                "text": "*Repository:*\n"+entities[0]
            }
        ]
    })
    smells = ""
    for r in results:
        smells = smells + r + "\n"
    # appending detected smells in the last execution
    blocks.append({
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*Date:*\n"+entities[1]
            },
            {
                "type": "mrkdwn",
                "text": "*Results:*\n"+smells
            }
        ]
    })

    return {
        "channel": channel,
        "blocks": blocks
    }

# building the message containing basic information about community smells
def build_info_message(channel, user):
    lang = LanguageHandler().get_current_language()
    
    blocks = []
    if lang == "en":
        text = "Hi " + user + " :wave:"
    elif lang == "it":
        text = "Ciao " + user + " :wave:"
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True
        }
    })

    if lang == "en":
        text = "These are the *community smells* I can detect in your development communities:"
    elif lang == "it":
        text = "Questi sono i *community smells* che riesco a individuare nelle vostre community:"
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    })
    blocks.append({
        "type": "divider"
    })

    if lang == "en":
        fileName = 'src/community_smells.json'
    elif lang == "it":
        fileName = 'src/community_smells_it.json'
    with open(fileName) as fp:
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
    if lang == "en":
        text = "If you want to remain up-to-date, please follow us on our social networks:\n -Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab> \t -Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab> \t -Website: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io> \n Also, feel free to get in touch with us to have a discussion about the subject by sending us an email at slambiase@unisa.it!"
    elif lang == "it":
        text = "Se volete rimanere aggiornati, seguite i canali social:\n -Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab> \t -Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab> \t -Sito web: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io> \n Inoltre, sentitevi liberi di mettervi in contatto con noi per discutere dell'argomento inviandoci una mail a slambiase@unisa.it!"
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    })
    return {
        "channel": channel,
        "blocks": blocks
    }

def build_error_message(channel, user):
    lang = LanguageHandler().get_current_language()
    
    if lang == "en":
        text = "Hi "+user+", I'm sorry but I did not understand your intent. Please be more specific!"
    elif lang == "it":
        text = "Ciao "+user+", mi dispiace ma non sono riuscito a comprendere il suo intent. La prego di essere più specifico!"
    return {
        "channel": channel,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
    }

# this function will format the message basing on the intent
def build_message(results, user, channel, intent, entities):
    username = user.get('profile').get('first_name')
    if intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
        response = build_cs_message(
            results, channel, username, entities)
        return response
    elif intent == CadocsIntents.Report:
        response = build_report_message(
            channel, entities[2], results, username, entities)
        return response
    elif intent == CadocsIntents.Info:
        response = build_info_message(channel, username)
        return response