import asyncio
import base64
import json
import pyaudio
import pvporcupine
import struct
import websockets

assembly_key = ''
porcupine_key = ""

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

                    if silence_counter >= 5:  # Adjust this threshold as needed
                        print("Brp")
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
