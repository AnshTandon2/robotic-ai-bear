import asyncio
import cv2
import websockets
import base64

async def send_video_stream(websocket):
    cap = cv2.VideoCapture(0)  # Open the default camera (change the index if you have multiple cameras)

    while cap.isOpened():
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            break

        # Convert frame to base64 string
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)

        # Send frame as base64 string over WebSocket
        await websocket.send(jpg_as_text)

    cap.release()

async def connect_to_websocket():
    uri = "wss://api.hume.ai/v0/stream/models"  # Replace with your WebSocket server URL

    try:
        async with websockets.connect(uri) as websocket:
            # Connection established
            print("Connected to WebSocket server")
            
            # Start sending video stream
            await send_video_stream(websocket)
            
    except Exception as e:
        print("Failed to connect to WebSocket server:", e)

# Run the WebSocket client
asyncio.run(connect_to_websocket())
