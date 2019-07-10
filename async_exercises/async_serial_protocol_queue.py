# thanks to: https://github.com/zmitchell/async-serial

import asyncio
from functools import partial

import serial_asyncio


class Reader(asyncio.Protocol):
    def __init__(self, q) -> None:
        """ Store data inside the queue. """
        super().__init__()
        self.transport = None
        self.buf = None
        self.msgs_recvd = None
        self.q = q

    def connection_made(self, transport) -> None:
        """ Store the serial transport and prepare to receive data. """
        self.transport = transport
        self.buf = bytes()
        self.msgs_recvd = 0     # any messages  aren't received yet!
        print("Reader connection created")

    def data_received(self, data: bytes) -> None:
        """ Store chacters until a newline received """
        self.buf += data
        if b'\n' in self.buf:
            lines = self.buf.split(b'\n')
            self.buf = lines[-1]   # '\n' character
            for line in lines[:-1]:     # not included '\n' character
                asyncio.ensure_future(self.q.put(line))
                self.msgs_recvd += 1
        if self.msgs_recvd == 4:
            self.transport.close()

    def connection_lost(self, exc) -> None:
        print('Reader closed')


class Writer(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport) -> None:
        """ Store he serial transport and schedule the task to send data. """
        self.transport = transport
        print('Writer connection created')
        asyncio.ensure_future(self.send())
        print('Writer.send() scheduled')

    async def send(self):
        """ Send the newline-terminated data, one byte at a time """
        message = b'a\nb\nc\n'  # dummy initial message
        for b in message:
            await asyncio.sleep(0.5)
            self.transport.serial.write(bytes([b]))
            print(b'Writer sent: {bytes([b])}')
        self.transport.close()


# print received data
async def print_received(loop, q):
    counter = 0
    while counter < 4:
        msg = await q.get()
        print(f'Message received: {msg}')
        counter += 1
    loop.stop()

# start event queue
queue = asyncio.Queue()
reader_partial = partial(Reader, queue)
# start event loop
loop = asyncio.get_event_loop()
reader = serial_asyncio.create_serial_connection(loop, reader_partial, 'reader', baudrate=115200)
writer = serial_asyncio.create_serial_connection(loop, Writer, 'writer', baudrate=115200)
asyncio.ensure_future(reader)
print('Reader scheduled')
asyncio.ensure_future(writer)
print('Writer scheduled')
asyncio.ensure_future(print_received(loop, queue))
loop.run_forever()
print('Done')




