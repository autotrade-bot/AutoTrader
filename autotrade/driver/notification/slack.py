from slackclient import SlackClient
import os

class SlackNotificationDriver():

    token = os.environ.get("SLACK_API_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    notify_user = os.environ.get("SLACK_NOTIFY_USER")

    def __init__(self):
        self.client = SlackClient(self.token)

    def post(self, text):
        self.client.api_call(
            "chat.postMessage",
            channel=self.channel,
            parse=True,
            text="<@{0}> \n{1}".format(self.notify_user, text)
        )
