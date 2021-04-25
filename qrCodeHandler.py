
from logger import log, debug
import pyqrcodeng
import json
import sys
import cv2
import os

class QRHandler:

    def __init__(self,file_path):
        with open("config.json") as config_file:
            self.config = json.load(config_file)
        self.qr_path = file_path
        self.qr_code_content = []
        self.new_wrCode_path = []

    def readQrCode(self):
        log("start to read qr codes")
        detector = cv2.QRCodeDetector()
        for ticket in self.qr_path:
            img = cv2.imread(ticket)
            data, bbox, straight_qrcode = detector.detectAndDecode(img)
            self.qr_code_content.append(data)
            os.remove(ticket)
        if len(self.qr_code_content) < 1:
            log("no QRCodes were found")
        else:
                log("read all qr codes")

    def checkForDublicates(self):
        if len(self.qr_code_content) == len(set(self.qr_code_content)):
            log("no duplicates found")
        else:
            log("duplicates found. Can't continue.")
            sys.exit()
    
    def creatQRCode(self):
        for index, data in enumerate(self.qr_code_content):
            new_path = self.qr_path[index].replace(f"ticket no{index}.jpg", f"qr_code_no{index}.png")
            self.new_wrCode_path.append(new_path)
            #debug("creatQrCode", f"index: {index}, data: {data}")
            qr = pyqrcodeng.create(data)
            qr.png(new_path, self.config["QRSize"], quiet_zone=1)


    def handleQrCode(self):
        self.readQrCode()
        self.checkForDublicates()
        self.creatQRCode()
        return self.new_wrCode_path