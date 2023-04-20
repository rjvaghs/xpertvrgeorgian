from flask import Flask, request
import requests
import openai
import json
from characters import chars
import time

openai.api_key = "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"
completion = openai.Completion()


def write_json(data, filename='response.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def ask(question, character_name, chat_log):
    start_sequence = "\n" + character_name + ": "
    restart_sequence = "\n\nPerson:"
    session_prompt = "You are interrogating " + character_name + "\n" + "Description: " + chars[character_name]
    if chat_log is None:
        prompt_text = f'{session_prompt}{restart_sequence}: {question}{start_sequence}:'
    else:
        prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
      engine="davinci:ft-xpertvr-georgian-team-2023-02-01-19-26-22",
      prompt=prompt_text,
      temperature=0.5,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.3,
      stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, character_name, chat_log):
    start_sequence = "\n" + character_name + ": "
    restart_sequence = "\n\nPerson:"
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


chat_log = None


def dialog(question, character_name):
    global chat_log
    answer = ask(question, character_name, chat_log)
    chat_log = append_interaction_to_chat_log(question, answer, character_name, chat_log)
    return answer


app = Flask(__name__)


@app.route('/api', methods=['POST'])
def process_message():  # put application's code here
    message = request.form['message']
    character_name = request.form['character_name']
    response = dialog(message, character_name)
    return response


if __name__ == '__main__':
    app.run()


