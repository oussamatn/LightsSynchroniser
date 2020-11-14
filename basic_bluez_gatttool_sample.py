#!/usr/bin/env python
from __future__ import print_function

import binascii
import pygatt

YOUR_DEVICE_ADDRESS = "07:1A:00:00:0E:C4"
# Many devices, e.g. Fitbit, use random addressing - this is required to
# connect.


adapter = pygatt.GATTToolBackend()
adapter.start()
device = adapter.connect(YOUR_DEVICE_ADDRESS)

for uuid in device.discover_characteristics().keys():
    print("Read UUID %s: %s" % (uuid, device.char_read(uuid)))
