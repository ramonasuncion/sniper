import groq
from groq import Groq
import os
from dotenv import load_dotenv


DEFAULT_MODEL = "llama-3.3-70b-versatile"

# GroqLLM ai initializes api key and takes any query in the review code function
# Currently using the free plan for Groq 
class GroqLLM:
    def __init__(self, curr_model=DEFAULT_MODEL):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.curr_model = curr_model

    def review_code(self, code_block: str) -> str | None:
        """Reviews the provided code_block using the specified model"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code reviewer. Analyze the code for bugs, security issues, and best practices."
                    },
                    {
                        "role": "user",
                        "content": code_block,
                    }
                ],
                model=self.curr_model,
            )
            return chat_completion.choices[0].message.content

        except groq.APIConnectionError as e:
            print(f"The server could not be reached: {e}")
            return None
        except groq.RateLimitError as e:
            print(f"The rate limit has been reached: {e}")
            return None
        except groq.APIStatusError as e:
            print(f"API Error (status:{e.status_code}): {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

