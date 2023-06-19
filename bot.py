import os
import slack
import openai
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response

from slackeventsapi import SlackEventAdapter



env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/ask', methods=['POST'])
def message_count():
    data = request.form
    channel_id = data.get('channel_id')

    textPromt = data.get('text')
    
    gptResponse = callGPT(textPromt)
    client.chat_postMessage(channel=channel_id, text=gptResponse)

    return Response(), 200

def callGPT(prompt):
    openai.api_key = os.environ['OPEN_AI']

    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        temperature = 1,
        max_tokens = 2000,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    text = ''
    if "choices" in response and response["choices"]:
        if "text" in response["choices"][0]:
            text = response["choices"][0]["text"]
        else:
            text = ''
    else:
        text = ''

    return text


if __name__ == "__main__":
    app.run(debug=True)
