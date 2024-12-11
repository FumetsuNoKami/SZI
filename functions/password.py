from tkinter import simpledialog
import tkinter as tk

from functions.expiration_date import get_current_month

def check_password():
    month_number = get_current_month()
    if month_number is None:
        print("Ошибка: не удалось получить текущий месяц.")
        return False

    passwords_by_month = {
        1: "jan_pass_43kX",
        2: "feb_pass_wQ84",
        3: "mar_pass_29LZ",
        4: "apr_pass_fG12",
        5: "may_pass_98Xy",
        6: "jun_pass_Ue47",
        7: "jul_pass_kP93",
        8: "aug_pass_qB21",
        9: "sep_pass_Tm56",
        10: "oct_pass_Lz77",
        11: "nov_pass_Ew32",
        12: "dec_pass_Vj89"
    }

    correct_password = passwords_by_month.get(month_number)

    root = tk.Tk()
    root.withdraw()

    entered_password = simpledialog.askstring("Пароль", f"Введите пароль для месяца {month_number}:", show='*')

    if entered_password == correct_password:
        return True
    else:
        return False