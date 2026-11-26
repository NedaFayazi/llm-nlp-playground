
import dotenv
import os
from openai import OpenAI
#import tiktoken
#from transformers import AutoTokenizer
import time

dotenv.load_dotenv()

OPENROUTER_API_KEY =os.getenv("OPENROUTER_API_KEY")
BASE_URL=os.getenv("BASE_URL")



class ChatSample:
    def __init__(self):
        self.llm = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=BASE_URL,
        )

        self.messages = [{
            "role": "system",
            "content": 'You are an assistant. your name is golab_bot, introduce yourself in the first message. give precise answers',
        }]

        self.total_tokens = 0
        self.iterations = 0

    def trimmed_messages(self, max_number = 4):
        if len(self.messages) < max_number:
            return

                    #[expression for item in iterable if condition]
        system_msg = [m for m in self.messages if m["role"] == "system"]
        user_assistant_msgs = [m for m in self.messages if m["role"] != "system"]
        trimmed_msgs = user_assistant_msgs[-max_number:]

        self.messages = [*system_msg, *trimmed_msgs]

    def summarized_messages(self):
        if len(self.messages) % 5 != 0:
            return
        system_msg = [m for m in self.messages if m["role"] == "system"]
        user_assistant_msgs = [m for m in self.messages if m["role"] != "system"]

        initial_msgs, rest_msgs = (user_assistant_msgs[0:5], user_assistant_msgs[5:])

        response = self.llm.chat.completions.create(
            model='openai/gpt-oss-20b',
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following text concisely, keeping key facts and decisions."
                }, *initial_msgs,
            ]
        )
        summarized_msgs = {
                "role": "system",
                "content": f'''this is the summary of the first 5 msgs: {response.choices[0].message.content}'''
            }

        self.messages = [*system_msg, summarized_msgs, *rest_msgs]


    def bot(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        response = self.llm.chat.completions.create(
            model='openai/gpt-oss-20b',
            messages = self.messages,
            stream = True,
            stream_options = {"include_usage": True}
        )
        ai_response = ''
        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta.content
                if  delta:
                    print(delta, end= '', flush=True)
                    time.sleep(0.05)
                    ai_response += delta
            if chunk.usage:
                self.total_tokens += chunk.usage.total_tokens
        print()


        #ai_response = response.choices[0].message.content
        self.messages.append({
            "role": "assistant",
            "content": ai_response
        })

        #self.trimmed_messages()
        self.summarized_messages()
        return ai_response

    def chat(self):
        #encoding = tiktoken.get_encoding('cl100k_base')
        #encoding = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

        while True:
            self.iterations += 1
            #if self.total_tokens > 300:
                #print('You have exceeded the maximum token limit')
                #break
            user_input = input('Enter your message: (to leave press "q"): ').strip().lower()

            if user_input == 'q':
                print('GoodLuck!')
                break

            self.bot(user_input)
            #bot_response = self.bot(user_input)
            #print(encoding.encode(user_input))
            #print(len(encoding.encode(user_input)))
            #print(bot_response)

    def report(self):
        for message in self.messages:
            print(message)

        print(f'Total tokens: {self.total_tokens}')


def main():
    bot = ChatSample()
    bot.chat()
    bot.report()

if __name__ == '__main__':
    main()