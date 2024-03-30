import asyncio

from hume import HumeStreamClient, StreamSocket
from hume.models.config import ProsodyConfig

async def main():
    client = HumeStreamClient("bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd")
    config = ProsodyConfig()
    async with client.connect([config]) as socket:
        result = await socket.send_file("WIN_20240330_11_59_42_Pro.mp4")
        print(result)

asyncio.run(main())

