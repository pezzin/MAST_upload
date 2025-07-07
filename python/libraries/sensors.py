import time
import requests  # nuova dipendenza per inviare HTTP POST
from PetoiRobot import *
from datetime import datetime

def read_sensors(sensors: list, read_time: int, label: str = '', server_url: str = None):
    """
    Function to read all sensors and send each data point via HTTP POST to a server.
    * sensors[list]: list of connected sensors
    * read_time[int]: time (in seconds) for the acquisition
    * label[str]: label for AI
    * server_url[str]: endpoint to send data
    """

    if len(sensors) == 0:
        raise ValueError('Please specify at least one sensor.')

    for sensor in sensors:
        if sensor not in ['pir', 'touch', 'light', 'ir']:
            raise ValueError(
                'Specified an unknown sensor type. Available sensors include: pir, touch, light, ir.')

    if 'touch' in sensors and 'pir' in sensors:
        raise ValueError('Please specify only one type of digital sensor.')

    wait_for = 1

    if read_time < wait_for:
        raise ValueError('Please specify a read_time >= 1')

    print('----------------------------')
    print('Starting data acquisition...')

    for _ in range(round(read_time/wait_for)):
        tmp = {}
        tmp['timestamp'] = datetime.now().isoformat()

        if 'pir' in sensors:
            tmp['pir'] = readDigitalValue(6)
        else:
            tmp['pir'] = -1

        if 'touch' in sensors:
            tmp['touch_right'] = readDigitalValue(6)
            tmp['touch_left'] = readDigitalValue(7)
        else:
            tmp['touch_right'] = -1
            tmp['touch_left'] = -1

        if 'light' in sensors:
            tmp['light_right'] = readAnalogValue(16)
            tmp['light_left'] = readAnalogValue(17)
        else:
            tmp['light_right'] = -1
            tmp['light_left'] = -1

        if 'ir' in sensors:
            tmp['ir_right'] = readAnalogValue(16)
            tmp['ir_left'] = readAnalogValue(17)
        else:
            tmp['ir_right'] = -1
            tmp['ir_left'] = -1

        tmp['label'] = label

        print(f'Acquired data: {tmp}')

        # Send data via HTTP POST
        if server_url:
            try:
                response = requests.post(server_url, json=[tmp])
                if response.status_code == 200:
                    print(f"Data sent successfully to {server_url}")
                else:
                    print(f"Server error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Failed to send data: {e}")

        time.sleep(wait_for)

    print('Finished data acquisition')
    print('----------------------------')


def main():
    sensors = ['pir', 'light']
    read_time = 10
    label = 'test'
    server_url = 'https://YOUR_ENDPOINT_URL/api/data'  # sostituisci con il tuo vero endpoint

    read_sensors(sensors, read_time, label, server_url)


if __name__ == '__main__':
    main()
