import pygatt 
import time
# The BGAPI backend will attempt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.backends.GATTToolBackend()
#MAC :  07:1A:00:00:0E:C4
try:
	adapter.start()
	device = adapter.connect('07:1A:00:00:0E:C4',timeout=3)
	charact = device.discover_characteristics().keys()
	print(charact)
	#0x56,0xFF,0x00,0xFF,0x00,0xF0,0xAA
	#char-write-cmd 0x0009 0xCC,0x24,0x33
	time.sleep(1)
	# OFF
	device.char_write('0000ffd9-0000-1000-8000-00805f9b34fb',bytearray([0xCC,0x24,0x33]))
	time.sleep(1)
	#Turn On
	device.char_write('0000ffd9-0000-1000-8000-00805f9b34fb',bytearray([0xCC,0x23,0x33]))
	time.sleep(1)
	# Set built-in mode
	#device.char_write('0000ffd9-0000-1000-8000-00805f9b34fb',bytearray([0xBB,0x38,0x10,0x44]))
	#RGB mode
	cmd = bytearray([0x56,0xFF,0x00,0xFF,0x00,0xF0,0xAA])
	#cmd = bytearray([0x66,0x15,0x23,0x41,0x20,0x00,0xFF,0x00,0x00,0x00,0x06,0x99])
	device.char_write('0000ffd9-0000-1000-8000-00805f9b34fb',cmd)
	time.sleep(1)
except Exception:
	print("exception")    
finally:
	adapter.stop()
