import numpy as np
from tkinter import *
from tkinter import ttk


def main():
    window = Tk()
    frame = ttk.Frame(window, padding=10)
    window.geometry("800x100")
    frame.grid()

    ttk.Label(frame, text="Введите сообщение для кодирования").grid(column=0, row=0)
    ttk.Label(frame, text="Введите сообщение для декодирования").grid(column=0, row=1)

    entry1 = ttk.Entry(frame, width=12)
    entry1.grid(column=1, row=0)

    entry2 = ttk.Entry(frame, width=24)
    entry2.grid(column=1, row=1)

    code = ttk.Label(frame, text='')
    code.grid(column=3, row=0)

    decode = ttk.Label(frame, text='')
    decode.grid(column=3, row=1)

    ttk.Button(frame, text="Закодировать", command=lambda: coding(entry1, code)).grid(column=2, row=0)
    ttk.Button(frame, text="Декодировать", command=lambda: decoding(entry2, decode)).grid(column=2, row=1)

    window.mainloop()


def coding(entry, code_label):
    with open('matrix.txt', 'r') as f:
        matrix = np.array([list(map(int, f.readline().split())) for i in range(12)])

    code = entry.get()
    code = np.array([int(i) for i in code])
    coding_code = (code @ matrix) % 2
    message = ''
    for i in coding_code:
        message += str(i)
    code_label.config(text=message)


def decoding(entry, decode_label):
    with open("checker.txt", 'r') as f:
        matrix = np.array([list(map(int, f.readline().split())) for i in range(12)]).T

    code = entry.get()
    code = np.array([int(i) for i in code])
    syndrome = (code @ matrix) % 2

    message = ''
    errors = []
    if np.equal(syndrome, np.zeros(12)).all():
        message = 'Ошибок не обнаружено'
        decode_label.config(text=message)
        return
    if message == '':
        errors = find_one_error(start=0, syndrome=syndrome, matrix=matrix)
        print(f'1 errors =  {errors}')
    if not errors:
        errors = find_two_errors(start=0, syndrome=syndrome, matrix=matrix)
        print(f'2 errors =  {errors}')
    if not errors:
        errors = find_three_errors(syndrome=syndrome, matrix=matrix)
        print(f'3 errors =  {errors}')

    if not errors:
        message = 'Обнаружено более трех ошибок'
        decode_label.config(text=message)
    else:
        for i in errors:
            code[i] = 1 - code[1]
        result = ''
        for i in code:
          result += str(i)
        decode_label.config(text=f'Декодированное сообщение: {result[:12]}')


def find_one_error(*, start, syndrome, matrix):
    errors = []
    for i in range(start, len(matrix)):
        if np.equal(matrix[i], syndrome).all():
            errors.append(i)
            break
    return errors


def find_two_errors(*, start, syndrome, matrix):
    errors = []
    for i in range(start, len(matrix)):
        tmp = np.array([(syndrome[j] + matrix[i][j]) % 2 for j in range(len(syndrome))])
        print(tmp)
        error = find_one_error(start=i, syndrome=tmp, matrix=matrix)
        if error:
            errors.append(i)
            errors.append(error[0])
            break
    return errors


def find_three_errors(*, syndrome, matrix):
    errors = []
    for i in range(len(matrix)):
        tmp = np.array([(syndrome[j] + matrix[i][j]) % 2 for j in range(len(syndrome))])
        two_errors = find_two_errors(start=i, syndrome=tmp, matrix=matrix)
        if two_errors:
            errors.append(i)
            errors.append(two_errors[0])
            errors.append(two_errors[1])
            break
    return errors


if __name__ == '__main__':
    main()
