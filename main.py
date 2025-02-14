import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

def get_user_input():
    return input("Enter a topic to learn about (or 'exit' to quit): ")

def run(topic):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        return

    try:
        client = Groq(api_key=api_key)
        client = instructor.from_groq(client, mode=instructor.Mode.JSON)

        resp = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": f"Tell me about {topic}"}],
            response_model=Character,
        )
        print(resp.model_dump_json(indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        user_input = get_user_input()
        if user_input.lower() == 'exit':
            break
        run(user_input)