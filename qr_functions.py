import cv2
import re
import qrcode as qr
from datetime import datetime
import string
import random


def generate_random_string(length):
    return ''.join((random.choice(string.ascii_letters) for x in range(length)))


def read_qr(rgx, path='static/photo.jpg'):
    img = cv2.imread(path)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrqode = detector.detectAndDecode(img)
    if re.match(rgx, data) is not None:
        return data[9:11]
    else:
        return False


def generate_qr(data, filename=''):
    if not filename:
        time = datetime.strftime(datetime.now(), '%d%m%Y-%H%M%S')
        filename = f'image-qrdata-{data}-{time}'
    elif '.' in filename:
        filename = filename.split('.')[0]
    filename = f'static/generation/{filename}.png'

    data = str(data)
    three_letters_data = '0' * (3 - len(data)) + data
    complete_data = f'cvid{generate_random_string(4)}={three_letters_data}{generate_random_string(3)}'

    img = qr.make(str(complete_data))
    img.save(filename)