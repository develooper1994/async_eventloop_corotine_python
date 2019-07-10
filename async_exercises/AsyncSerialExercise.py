import asyncio
import serial_asyncio


class Writer(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        """ Store the serial transport and schedule the task to send data. """
        self.transport = transport
        print('Writer connection created')
        asyncio.ensure_future(self.send())
        print('Writer.send() established')

    def connection_lost(self, exc):
        print("Writer closed")

    async def send(self):
        """ Send four newline-terminated messages, one byte at a time. """
        message = b'a\nb\nc\n'
        for b in message:
            await asyncio.sleep(0.5)
            self.transport.serial.write(bytes([b]))
            print(f'Writer sent: {bytes([b])}')
        self.transport.close()


class Reader(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        """ Store the serial transport and prepare to receive data. """
        self.transport = transport
        self.buf = bytes()
        self.mesgs_recv = 0
        print('Reader connection established')

    def data_received(self, data: bytes) -> None:
        """ Store characters until a newline is received. """
        self.buf += data
        if b'\n' in self.buf:
            lines = self.buf.split(b'\n')
            for line in lines[:-1]:
                print(f'Reader received: {line.decode()}')
                self.mesgs_recv += 1
        if self.mesgs_recv == 4:
            self.transport.close()

    async def connection_lost(self, exc) -> None:
        print('Connection Closed')


try:
    loop = asyncio.get_event_loop()
    reader = serial_asyncio.create_serial_connection(loop, Reader, 'reader', baudrate=115200)
    writer = serial_asyncio.create_serial_connection(loop, Writer, 'writer', baudrate=115200)

    asyncio.ensure_future(reader)
    print('Reader scheduled')
    asyncio.ensure_future(writer)
    print('Writer scheduled')

    loop.call_later(10, loop.stop)
    loop.run_forever()
    print('Done')
except KeyboardInterrupt:
    pass
finally: pass
    #loop.close()
