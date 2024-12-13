import sys
from Layout.Layout import LoginWindow, app

import config
from datetime import datetime

import ntplib
import pytz

import subprocess

def get_disk_serial_number():
    try:
        output = subprocess.check_output('wmic diskdrive get serialnumber', shell=True)
        serial = output.decode().split("\n")[1].strip()[:-1]
        return serial
    except Exception as e:
        return None

def check_disk_serial(expected_serials):
    if get_disk_serial_number() in expected_serials:
        return True
    else:
        return False

def get_time_from_ntp():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request(
            'pool.ntp.org')
        ntp_time = datetime.fromtimestamp(response.tx_time,
                                          tz=pytz.timezone('UTC'))
        return ntp_time
    except Exception as e:
        print(f"Ошибка при обращении к NTP-серверу: {e}")
        return None


def check_expiration_date(expiration_date_str):
    expiration_date = datetime.strptime(expiration_date_str,"%Y-%m-%d").date()

    current_date = get_time_from_ntp()

    if current_date is None:
        print("Ошибка: не удалось получить текущую дату с NTP-сервера.")
        return False

    if current_date.date() <= expiration_date:
        return True
    else:
        return False


def get_current_month():
    current_time = get_time_from_ntp()
    if current_time is None:
        return None
    return current_time.month

def check_conditions():
    if not check_disk_serial(config.disk_serial_number):

        return False
    if not check_expiration_date(config.expiration_date):

        return False

    return True


window = LoginWindow(check_conditions())
window.show()
sys.exit(app.exec_())