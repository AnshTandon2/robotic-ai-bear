import asyncio
import websockets
import cv2
import base64
import sys
import json


hume_api_url = "wss://api.hume.ai/v0/stream/models"
api_key = "bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd"  

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Failed to open camera.")
    cap.release()
    sys.exit(1)

async def send_to_hume_api():
    async with websockets.connect(hume_api_url, extra_headers={"X-Hume-Api-Key": api_key}) as websocket:
        while True:
            print("Camera opened successfully:", cap.isOpened())
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            # Convert the frame to base64
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')
            # Define the payload with the necessary parameters
            payload = {
                "models": {
                    "language": {}
                },
                "raw_text": True,
                "data": img_base64  # Assuming you want to send image data
                # "models": Dict[str, Dict[str, Any]] = {
                #   "burst": {},
                #   "face": {
                #     "facs": {},
                #     "descriptions": {},
                #     "identify_faces": False,
                #     "fps_pred": 3,
                #     "prob_threshold": 3,
                #     "min_face_size": 3
                #   },
                #   "facemesh": {},
                #   "language": {
                #     "sentiment": {},
                #     "toxicity": {},
                #     "granularity": "string"
                #   },
                #   "prosody": {}
                # },
                # "stream_window_ms": 5000,
                # "reset_stream": False,
                # "raw_text": False,
                # "job_details": False,
                # "payload_id": "string"
            }
            # print("Pay load: ", payload)


            # Send the payload as a JSON-formatted string
            try:
              await websocket.send(json.dumps(payload))
            except Exception as e:
             print("Error sending payload:", e)
            

            print("Payload", payload)
            # add delay to socket time to ensure program doesn't time out
            await asyncio.sleep(0.1)
            # recieves response from the input
            response = await websocket.recv()
            outputs = json.loads(response)
            # Dump the outputs into sending.json
            with open('sending.json', 'w') as file:
              json.dump(outputs, file)
            cv2.imshow('Emotion Detection', frame)
            # exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Run the async function
asyncio.get_event_loop().run_until_complete(send_to_hume_api())