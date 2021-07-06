from slack import RTMClient
import requests
from stock_api import *
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
@RTMClient.run_on(event="message")
def stockbot(**payload):
    """
    This function triggers when someone sends
    a message on the slack
    """
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")

    # If a message is not send by the bot
    if bot_id == "":
        channel_id = data["channel"]

        # Extracting message send by the user on the slack
        text = data.get("text", "")
        text = text.split()
        response = ""
        """ 
        Prints out the list of commands that's avalible to the user
        """
        if "help" in text[1]:
            user = data.get("user", "")
            response = f"Hello <@{user}>! You look like you need some help :wave:\n"
            response += '>``` info [\'stock name\'] ... - Return the summary info of the stock ```\n'
            response += '>``` price [\'stock name\'] ... - State the current price of the stock ```\n'
            response += '>``` graph [\'stock name\'] ... - Displays the graph of the stock ```\n'
            response += 'Please note you can have multiple stock searches if you include spaces and you must mention me'
        elif "price" in text[1]:
            response = getPrice(text[2])
        elif "info" in text[1]:
            response = getInfo(text[2])
        elif "graph" in text[1]:
            message = getGraph(text[2])
            if(message != "I don't think this stock exists"):
                response = web_client.files_upload(
                    channels=channel_id,
                    file="plot.png",
                    title="Graph"
                )
            else:
                response = message 
        else:
            response = "I'm sorry I don't understand your command"
        # Sending m essage back to slack
        web_client.chat_postMessage(channel=channel_id, text=response)

try:
    rtm_client = RTMClient(token=os.environ['SLACK_TOKEN'])
    print("Bot is up and running!")
    rtm_client.start()
except Exception as err:
    print(err)