import json


# building of the message for the intent GetCommunitySmells or GetCommunitySmellsDate
def build_cs_message(smells, channel, user, entities):
    print(smells, entities)
    # blocks that will be displayed in slack
    blocks = []
    blocks.append(
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Hi "+user+" :wave:",
                "emoji": True
            }
        }
    )
    if len(entities) > 2:
        text = "These are the community smells we were able to detect in the repository " + \
            entities[0]+" starting from "+entities[1]+":"
    else:
        text = "These are the community smells we were able to detect in the repository " + \
            entities[0]+":"
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
    with open('src/community_smells.json') as fp:
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

    return {
        "channel": channel,
        "blocks": blocks
    }

# building the message for the Report intent
def build_report_message(channel, exec_type, results, user, entities):
    # blocks that will be displayed in slack
    blocks = []
    blocks.append(
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Hi "+user+" :wave:",
                "emoji": True
            }
        }
    )
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
    blocks = []
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Hi "+user+" :wave:",
            "emoji": True
        }
    })
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
    return {
        "channel": channel,
        "blocks": blocks
    }


def build_error_message(channel, user):
    return {
        "channel": channel,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi "+user+", I'm sorry but I did not understand your intent. Please be more specific!"
                }
            }
        ]
    }
