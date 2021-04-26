from getTicket_handler import getTicket
from email_handler import emailHandler
from qrCodeHandler import QRHandler
from pdf_handler import pdfHandler
from logger import log, debug
import time

def main():
    #The intercepted keyboard interrupt by Ctrl+C is converted into an exit of the program without error message.
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
    pdf_handler = pdfHandler(file_path)
    file_path = pdf_handler.converter()
    QR = QRHandler(file_path)
    file_path = QR.handleQrCode()
    pdf_handler.creatPDF(file_path)
    log("program has finished")

if __name__ == "__main__":
    main()
