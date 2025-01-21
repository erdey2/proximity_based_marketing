from bleak import BleakScanner

async def scan_beacons():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}, RSSI: {device.rssi}")

import asyncio
asyncio.run(scan_beacons())