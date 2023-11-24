import cv2


def read_qr(path='static/photo.jpg'):
    img = cv2.imread(path)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrqode = detector.detectAndDecode(img)
    return data
