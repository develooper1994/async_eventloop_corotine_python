import asyncio
import serial_asyncio


async def main():
    pass


async def send(writer, msgs):
    for msg in msgs:
        writer.write(msg)
        print(f'sent: {msg.decode().rstrip()}')
        await asyncio.sleep(0.5)
    writer.write(b'DONE\n')
    print('Done sending')


async def recv(reader):
    while True:
        msg = await reader.readuntil(b'\n')
        if msg

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

