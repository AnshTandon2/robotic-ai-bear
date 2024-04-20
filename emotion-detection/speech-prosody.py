import asyncio

from hume import HumeStreamClient, StreamSocket
from hume.models.config import ProsodyConfig

async def main():
  client = HumeStreamClient("bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd")
  config = ProsodyConfig()
  try:
    async with client.connect([config]) as socket:
      result = await socket.send_file("test-demo-3-hume.mov")
      print(result)
  except Exception as e:
    print(f"Error occurred while opening socket: {e}")

asyncio.run(main())
