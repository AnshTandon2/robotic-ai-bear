import asyncio
import base64
import json
import pyaudio
import pvporcupine
import struct
import websockets
import requests

assembly_key = 'ea370242ab8c4e96a77affd669e1bd00'
porcupine_key = "rxNAR+cOa0S34wc6Z0JwTUB3VwBs9UoxyeeRs73k9ddIU1Eeo9lvZg=="

# LLM stuff

def llm_response(q):
    """client = Groq(
        api_key="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"
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
        
    )"""
    

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
			{"role": "system", "content": "You are a helpful assistant."},
			{"role": "user", "content": q}
		]
    }
    
    response = requests.post(url, json=data, headers=headers)
    response = response.json()
    return response['choices'][0]['message']['content']

# Audio settings
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# AssemblyAI endpoint
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# Initialize PyAudio
p = pyaudio.PyAudio()

async def send_receive(stream):
    print(f'Connecting websocket to url ${URL}')
    silence_counter = 0  # Counter to track consecutive silence detections
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", assembly_key),),
        ping_interval=5,
        ping_timeout=20
    ) as ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            nonlocal silence_counter
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await ws.send(json_data)
                    if silence_counter >= 5:  # Adjust this threshold as needed
                        print("Stopping due to silence.")
                        break
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    break
                except Exception as e:
                    print("Error sending data: ", e)
                    break
                await asyncio.sleep(0.01)

        async def receive():
            nonlocal silence_counter
            while True:
                try: 
                    result_str = await ws.recv()
                    result = json.loads(result_str)
                    print(result['text'])
                    if result['text'] == "":
                        silence_counter += 1
                    else:
                        silence_counter = 0
                        final_query = result['text']

                    if silence_counter >= 5:  # Adjust this threshold as needed
                        print("this the final query: ", final_query)
                        llm_resp = llm_response(final_query)
                        print(llm_resp)
                        break
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    break
                except Exception as e:
                    print("Error receiving data: ", e)
                    break

        await asyncio.gather(send(), receive())

def start_listening():
    porcupine = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=["jarvis"], access_key=porcupine_key)

        audio_stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for wake word...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm_unpacked)
            if keyword_index >= 0:
                print("Wake word detected! Starting to send audio...")
                asyncio.run(send_receive(audio_stream))
                print("Resuming listening for wake word...")
                # The listening loop continues, allowing for the process to start over when the wake word is detected again

    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        p.terminate()

if __name__ == "__main__":
    start_listening()
