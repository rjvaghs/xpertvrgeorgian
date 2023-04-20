from characters import chars
import openai

openai.api_key = "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"
completion = openai.Completion()


class Conversations:
    chat_log = None

    def __init__(self, character_name):
        self.character_name = character_name

    def ask(self, question):
        start_sequence = "\n" + self.character_name + ": "
        restart_sequence = "\n\nPerson:"
        session_prompt = "You are " + self.character_name + "\n" + "Description: " + chars[self.character_name] + "\n A police officer is interrogating you"

        if Conversations.chat_log is None:
            prompt_text = f'{session_prompt}{restart_sequence}: {question}{start_sequence}:'
        else:
            prompt_text = f'{Conversations.chat_log}{restart_sequence}: {question}{start_sequence}:'
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
