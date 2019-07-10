# thanks to: https://github.com/zmitchell/async-serial

import asyncio
import serial_asyncio


async def main():
    reader, _ = await serial_asyncio.open_serial_connection(url='./reader', baudrate=57600)
    print('Reader created')
    _, writer = await serial_asyncio.open_serial_connection(url='./writer', baudrate=57600)
    print('Writer created')
    messages = [b'foo\n', b'bar\n', b'baz\n', b'qux\n']
    sent = send(writer, messages)
    received = recv(reader)
    await asyncio.wait([sent, received])


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
        if msg.rstrip() == b'DONE':
            print('message readed')
            break
        print(f'received message: {msg.rstrip().decode()}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

