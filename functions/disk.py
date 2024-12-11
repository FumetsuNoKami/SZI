import subprocess

def get_disk_serial_number():
    try:
        output = subprocess.check_output('wmic diskdrive get serialnumber', shell=True)
        serial = output.decode().split("\n")[1].strip()[:-1]
        return serial
    except Exception as e:
        return None

def check_disk_serial(expected_serial):
    serial_number = get_disk_serial_number()
    return serial_number == expected_serial