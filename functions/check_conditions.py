import config
from functions.disk import check_disk_serial
from functions.expiration_date import check_expiration_date
from functions.password import check_password

def check_conditions():
    if not check_disk_serial(config.disk_serial_number):
        print("Доступ с неразрешённого устройства")
        return False
    if not check_expiration_date(config.expiration_date):
        print("Срок действия истёк")
        return False
    if not check_password():
        print("Неверно введён пароль")
        return False

    print("Доступ разрешён")
    return True
