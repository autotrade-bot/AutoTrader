from slackclient import SlackClient
import os

class SlackNotificationDriver():

    token = os.environ.get("SLACK_API_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    notify_user = os.environ.get("SLACK_NOTIFY_USER")

    def __init__(self):
        self.client = SlackClient(self.token)
    """
    params:
        - name: action
          type: dict
          ex: {action: 'buy', amount: '0.001'}
        - name: price
          type: float
          ex: 20000000
        - name: position
          type: dict
        - ex: {side: "BUY", price: 200000, open_date: "2018-01-08T05:32:25.013"}
        - name: profit
          type: float
          ex: 100 or -200 (yen)
    """
    def post(self, action, price, position, profit):
        action_text = 'action: {0}, amount: {1}, now price: {2}\n'.format(action.get('action'), action.get('amount'), price)
        if position is not None:
            position_text = "now position  {0}, price: {1}, open date: {2}\n".format(position.get('side'), position.get('price'), position.get('open_date'))
            profit_text = "profit and loss: {0} yen\n".format(profit)
        else:
            position_text = ""
            profit_text = ""
        text = action_text + position_text + profit_text
        self.client.api_call(
            "chat.postMessage",
            channel=self.channel,
            parse=True,
            text="<@{0}> \n{1}".format(self.notify_user, text)
        )
