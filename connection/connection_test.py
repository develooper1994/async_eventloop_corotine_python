# %%
import serial
from serial import io
from serial import unicode
from serial import win32
from serial.tools import list_ports, miniterm
import asyncio
import serial_asyncio

# %%
portcomports = list_ports.comports(include_links=False)
allports = list(portItem.device for portItem in portcomports)
print(allports)

# %%
try:
    port = 'COM3'
    baudrate: int = 57600
    timeout = 2
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.timeout = timeout
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    print(ser.is_open)
    ser.close()
    print(ser.is_open)
    ser.open()
    print(ser.is_open)
except serial.serialutil.SerialException:
    print("disconnect and connect the serial port from computer")

# %%
print(ser)
ser.flush()
print(ser)
# %%
try:
    lines = ser.readlines(10)
    [print(line) for line in lines]
except serial.SerialException:
    ser.close()
    ser.open()
    print("Serial connection interrupted")
# %%
ser.write(b"\nroot\nroot")
# %%
miniterm.ask_for_port()


# %% *asyncio* | *serial_asyncio*

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print('data received', repr(data))
        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')


port = 'COM3'
baudrate = 57600

eventloop = asyncio.get_event_loop()
AsyncSerial = serial_asyncio.create_serial_connection(eventloop, Output, port, baudrate)
eventloop.run_until_complete(AsyncSerial)
eventloop.run_forever()
eventloop.close()
