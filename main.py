from getTicket_handler import getTicket
from email_handler import emailHandler
from qrCodeHandler import QRHandler
from pdf_handler import pdfHandler
from logger import log, debug
import time

try:
    print(" \n          eTicket creator by Tom Ole Haelbich\n \n")
    print("The QRCodes on the tickets are provided by the ticket provider eveeno.com")
    print("If you haven't read the documentation on Github yet, please exit this program by pressing ctr+c. \n")
    time.sleep(10)
except KeyboardInterrupt:
    print("You can restart the program when you are confident with it.")

ticketHandler = getTicket()
ticketHandler.main()
emailClient = emailHandler()
file_path = emailClient.startEmailHandler()
pdfHandler = pdfHandler(file_path)
file_path = pdfHandler.converter()
QR = QRHandler(file_path)
file_path = QR.handleQrCode()
pdfHandler.creatPDF(file_path)
log("program has finished")
