

# building of the message for the intent GetCommunitySmells
def get_cs_message(smells, channel, user, repo):
    # mocked strategies
    strategies = ["str1", "str2"]
    # block of the message
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
    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "This is the community smells we were able to detect in the repository "+repo+" :",
                "emoji": True
            }
        }
    )
    # appending blocks for each smell detected
    for s in smells:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": s
                }
            }
        )
    blocks.append({
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "We suggest you the following strategies:",
                    "emoji": True
                }
            })
    # appending strategies blocks for each smell
    for s in smells:
            blocks.append({
                "type": "divider"
            })

            blocks.append({
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "For "+s+", you could try:"
                }
            })        
            for st in strategies:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": st
                    }
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
        "channel":channel,
        "blocks": blocks
    }

def build_report_message(channel, exec_type, results, user, repo):
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
				"emoji": true
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
					"text": "*Repository:*\n"+repo
				}
			]
		})
    smells = ""
    for r in results:
        smells = smells + "r\n"
    blocks.append({
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Date:*\n"+date
				},
				{
					"type": "mrkdwn",
					"text": "*Results:*\n"+smells
				}
			]
		})
                    
    return {
        "channel":channel,
        "blocks": blocks
    }
