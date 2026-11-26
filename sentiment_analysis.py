import dotenv
import os
from openai import OpenAI
from transformers import pipeline

dotenv.load_dotenv()

OPENROUTER_API_KEY =os.getenv("OPENROUTER_API_KEY")
BASE_URL=os.getenv("BASE_URL")

class Analyzer:
    def __init__(self):
        self.llm = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=BASE_URL,
        )

        self.messages = [
            {
            "role": "system",
            "content": 'sentiment the input message as negative, positive or neutral',
            },

            {
                "role": "user",
                "content": "I love spending time with my family."
            },
            {
                "role": "assistant",
                "content": "Positive"
            },
            {
                "role": "user",
                "content": "I am disappointed with the results."
            },
            {
                "role": "assistant",
                "content": "Negative"
            },
            {
                "role": "user",
                "content": "The meeting starts at 9 AM."
            },
            {
                "role": "assistant",
                "content": "Neutral"
            }

        ]

    def sentiment_analysis(self, text):
        response = self.llm.chat.completions.create(
            model='openai/gpt-oss-20b',
            temperature = 0.1,
            messages=[
                *self.messages,
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content


def main():
    analyzer = Analyzer()
    sentiment = analyzer.sentiment_analysis('Every day is a new chance to become the best version of yourself')
    print(sentiment)

if __name__ == "__main__":
    main()