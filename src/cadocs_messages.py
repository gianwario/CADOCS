

# building of the message for the intent GetCommunitySmells or GetCommunitySmellsDate
# TODO: include DATE param
def build_cs_message(smells, channel, user, entities):
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
                "text": "This is the community smells we were able to detect in the repository "+entities[0]+" :",
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

def build_report_message(channel, exec_type, results, user, entities):
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
        "channel":channel,
        "blocks": blocks
    }

def build_info_message(channel, user):
    return {
    "channel": channel,
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Hi "+user+" :wave:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Since *community smells* are a recent introduction in the Software Engineering, i can only detect the following ten:"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn", 
				"text": "*Organizational Silo Effect*\n:tractor::corn: - OSE\n bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",  
				"text": "*Black-cloud Effect*\n:black_medium_square::cloud: - BCE\n bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn", 
				"text": "*Prima-donnas Effect*\n:princess::ring: - PDE\n bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "If you want to learn more about *community smells*, you can visit the following link:\n https://boh \n Also, feel free to get in touch with us to have a discussion about the subject! "
			}
		}
	]
}