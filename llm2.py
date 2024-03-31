import requests

def get_openai_chat_response(messages):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_OPENAI_API_KEY_HERE"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Example usage
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
response = get_openai_chat_response(messages)
print(response)
