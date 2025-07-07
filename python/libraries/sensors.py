import time
import csv
import os
import requests
from PetoiRobot import *
from datetime import datetime
import platform


def read_sensors(sensors: list, read_time: int, label: str = '', server_url: str = None):
    """
    Function to read all sensors and send each data point via HTTP POST to a server.
    * sensors[list]: list of connected sensors
    * read_time[int]: time (in seconds) for the acquisition
    * label[str]: label for AI
    * server_url[str]: endpoint to send data

    Returns collected data as a list of dicts.
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

    data = []

    print('----------------------------')
    print('Starting data acquisition...')
    for _ in range(round(read_time / wait_for)):

        tmp = {}
        tmp['timestamp'] = datetime.now().isoformat()

        # PIR
        if 'pir' in sensors:
            tmp['pir'] = readDigitalValue(6)
        else:
            tmp['pir'] = -1

        # TOUCH
        if 'touch' in sensors:
            tmp['touch_right'] = readDigitalValue(6)
            tmp['touch_left'] = readDigitalValue(7)
        else:
            tmp['touch_right'] = -1
            tmp['touch_left'] = -1

        # LIGHT
        if 'light' in sensors:
            tmp['light_right'] = readAnalogValue(16)
            tmp['light_left'] = readAnalogValue(17)
        else:
            tmp['light_right'] = -1
            tmp['light_left'] = -1

        # IR
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
                    print(f"✅ Data sent successfully to {server_url}")
                else:
                    print(f"❌ Server error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"❌ Failed to send data: {e}")

        data.append(tmp)
        time.sleep(wait_for)

    print('Finished data acquisition')
    print('----------------------------')

    return data


def save_sensor_data(data: list, filename: str):
    """
    Function to save the data locally in csv format.
    """

    if len(data) == 0:
        raise ValueError('Please provide some data')

    file_ext = '.csv'

    # Detect platform-specific home directory
    if platform.system() == "Windows":
        sep = '\\'
        home_dir = os.getenv('HOMEDRIVE')
        home_path = os.getenv('HOMEPATH')
        config_dir = home_dir + home_path
    else:
        sep = '/'
        home = os.getenv('HOME')
        config_dir = home

    data_dir = config_dir + sep + 'sensor_data'

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_dir = data_dir + sep + filename + file_ext
    keys = data[0].keys()

    if os.path.exists(file_dir):
        cnt = 1
        while True:
            file_dir = data_dir + sep + f"{filename}-{cnt}{file_ext}"
            if not os.path.exists(file_dir):
                break
            cnt += 1

    print('Saving data locally...')
    with open(file_dir, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f'✅ File saved successfully at {file_dir}')

    return None


def main():
    sensors = ['pir', 'light']
    read_time = 10
    label = 'test'
    server_url = 'https://petoiupload.vercel.app/api/data'

    # Read sensors and send data
    data = read_sensors(sensors, read_time, label, server_url)

    # Optionally, save a local copy
    save_sensor_data(data, 'test')


if __name__ == '__main__':
    main()
