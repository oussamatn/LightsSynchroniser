import asyncio
from bleak import BleakClient
from bleak import _logger as logger

address_ledstrip = "07:1A:00:00:0E:C4"
IO_DATA_CHAR_UUID = "0000ffd9-0000-1000-8000-00805f9b34fb"
state_off = bytearray([0xCC,0x24,0x33])
state_on  = bytearray([0xCC,0x23,0x33])
async def run(address_ledstrip):
    async with BleakClient(address_ledstrip) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))
        await client.write_gatt_char(IO_DATA_CHAR_UUID, state_on)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address_ledstrip))