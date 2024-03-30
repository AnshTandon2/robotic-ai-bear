import os

from groq import Groq

def llm_response(q):
    client = Groq(
        api_key="",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "you are jarvis: a talking dog for kids. you give 1-2 sentence responses"
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": q,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    return chat_completion.choices[0].message.content
