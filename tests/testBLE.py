import asyncio
from bleak import BleakClient
from bleak import _logger as logger

address = "07:1A:00:00:0E:C4"
IO_DATA_CHAR_UUID = "0000ffd9-0000-1000-8000-00805f9b34fb"
write_value = bytearray([0xCC,0x23,0x33])

async def run(address):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))
        await client.write_gatt_char(IO_DATA_CHAR_UUID, write_value)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))