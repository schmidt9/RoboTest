import asyncio
import time
from bleak import BleakScanner, BleakClient

# https://github.com/hbldh/bleak/blob/develop/examples/uart_service.py
# https://forums.raspberrypi.com/viewtopic.php?t=339462

def handle_disconnect(_: BleakClient):
    print("Device was disconnected, goodbye.")

async def main():
    device_name = "BT24"
    print(f"looking for device named '{device_name}'...")
    
    device = await BleakScanner.find_device_by_name(device_name)

    if device is None:
        print(f"device named '{device_name}' not found")
        return
    else:
        print(f"device found: '{device}'")

    async with BleakClient(device.address, pair=True, disconnected_callback=handle_disconnect) as client:
        print(f"connected as client '{client}'")

        for service in client.services:
            print("Service {0}: {1}".format(service.uuid, service.description))

            print("\tCharacteristics:")
            
            for characteristic in service.characteristics:
                print(f"\t{characteristic}")

                print(f"\t\tProperties:")

                for prop in characteristic.properties:
                    print(f"\t\t{prop}")

                    if prop == "write" and characteristic.handle == 24:
                        data = "F" # forward command
                        payload = data.encode("utf-8")
                        print(f"Writing '{payload}'")
                        await client.write_gatt_char(characteristic.uuid, payload)

                        time.sleep(0.5)
                        data = "S" # stop command
                        payload = data.encode("utf-8")
                        print(f"Writing '{payload}'")
                        await client.write_gatt_char(characteristic.uuid, payload)
                        

asyncio.run(main())
