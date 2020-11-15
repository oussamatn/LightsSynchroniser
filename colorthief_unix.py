import pyscreenshot as ImageGrab
from PIL import Image
from queue import Queue
import threading
import sys
import pygatt
import time
from yeelight import Bulb
exit_signal_received = False

#thread to send values
def color_setter_thread(bulb_led,device,queue):
	
	try:
		while not exit_signal_received:
			if isinstance(queue, Queue):
				try:
					color = queue.get(timeout=5)
				except:
					continue
				if isinstance(color, list):
					if isinstance(bulb_led,Bulb) :
						bulb_led.set_rgb(color[0], color[1], color[2])
					if isinstance(device,ble_device_type) :
						device.char_write('0000ffd9-0000-1000-8000-00805f9b34fb',bytearray([0x56, color[0], color[1], color[2], 0x00, 0xF0, 0xAA]))
	except KeyboardInterrupt:
		pass

#exit handler 
def terminate_handler(bulb_led,device):
	global exit_signal_received
	if isinstance(bulb_led,Bulb):
		bulb_led.stop_music()
	if isinstance(device,ble_device_type) :
		adapter.stop()
	print("exit")
	exit_signal_received = True        
# start 


queue = Queue(maxsize=1)
#BLE connection
adapter = pygatt.backends.GATTToolBackend()
adapter.start()
device = adapter.connect('07:1A:00:00:0E:C4',timeout=3)
device.char_write('0000ffd9-0000-1000-8000-00805f9b34fb',bytearray([0xCC,0x23,0x33]))

#Yeelight Connection
bulb_led = Bulb("192.168.1.72",effect="smooth")
bulb_led.start_music(2000)

time.sleep(1)
t = threading.Thread(name="color_change_thread", target=color_setter_thread, args=(bulb_led,device,queue,))
t.start()
ble_device_type = pygatt.backends.gatttool.device.GATTToolBLEDevice
diff = 10
width = 32*16
height = 32*9
key_color = None
while not exit_signal_received:
	try:
		
		im = ImageGrab.grab(backend="pygdk3", childprocess=False)
		resized_img = im.resize((width, height), Image.BILINEAR)
		resize = 150
		result = resized_img.convert('P', palette=Image.ADAPTIVE, colors=1)
		result.putalpha(0)
		colors = result.getcolors(resize * resize)
		dominant_color = colors[0][1][:3]
		if key_color is None:
			key_color = dominant_color
		else:
			if abs(dominant_color[0] - key_color[0]) < diff\
				and abs(dominant_color[1] - key_color[1]) < diff \
					and abs(dominant_color[2] - key_color[2]) < diff:
				continue
			else:
				key_color = dominant_color

		queue.put([dominant_color[0], dominant_color[1], dominant_color[2]])

	except KeyboardInterrupt:
		terminate_handler(bulb_led,device)
	except Exception:
		print("exception")
