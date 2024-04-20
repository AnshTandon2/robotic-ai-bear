import asyncio
import websockets
import cv2
import base64
import sys
import json

# Define the Hume API endpoint
hume_api_url = "wss://api.hume.ai/v0/stream/models"
# Define your API key
api_key = "bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd"  # Replace with your actual API key
# Open the computer's camera
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
            }
            print("error here")
            # Send the payload as a JSON-formatted string
            try:
              await websocket.send(json.dumps(payload))
            except Exception as e:
             print("Error sending payload:", e)

            print("what is happening")
            # Set ping_timeout to None to prevent socket timeout
            await websocket.ping()
            await asyncio.sleep(0)  # Add a small delay to prevent blocking
            print("whatasdlfkj")
            # Receive the response
            response = await websocket.recv()
            outputs = json.loads(response)
            # Dump the outputs into sending.json
            with open('sending.json', 'w') as file:
              json.dump(outputs, file)

            # Process the outputs as needed


            # Display the frame with the detected emotions
            cv2.imshow('Emotion Detection', frame)
            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

# Run the async function
asyncio.get_event_loop().run_until_complete(send_to_hume_api())
