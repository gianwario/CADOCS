import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('xoxb-3537687436610-3550389206065-Qg2pPAEixOyo15Vy4O3G7xgb')

slack_client = SlackClient(SLACK_TOKEN)

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    print(channels_call)
    if channels_call.get('ok'):
        return channels_call['channels']
    return None 

if __name__ == '__main__':
    channels = list_channels()
    if channels:
        print("Channels: ")
        for c in channels:
            print(c['name'] + " (" + c['id'] + ")")
    else:
        print("Unable to authenticate.")