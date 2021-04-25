from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from logger import log, debug
import json
import os

class pdfHandler:
    def __init__(self, file_path):
        self.ticket_file_pdf = file_path
        self.ticket_file_jpg = []
        with open("config.json") as config_file:
            self.config = json.load(config_file)

    def converter(self):
        log("start to convert pdfs to jpg")
        for ticket_pdf in self.ticket_file_pdf:
            ticket_jpg = convert_from_path(ticket_pdf, 350)
            new_path = ticket_pdf.replace("pdf", "jpg")
            self.ticket_file_jpg.append(new_path)
            for img in ticket_jpg:
                img.save(new_path, "JPEG")
            os.remove(ticket_pdf)
        log("converted all pdf")
        return self.ticket_file_jpg

    def getPath(self,ticket_id=0):
        abs_path = os.getcwd()
        media_folder = os.path.join(abs_path,'media')
        media_folder = os.path.join(media_folder,self.config["event"])
        if not os.path.isdir(media_folder):
            os.mkdir(media_folder)
        file_name = f"{self.config['event']} ticket no. {ticket_id}.pdf"
        media_path = os.path.join(media_folder, file_name)

        abs_path = os.getcwd()
        input_folder = os.path.join(abs_path,'media')
        input_folder = os.path.join(input_folder,'ticket template')
        if not os.path.isdir(input_folder):
            os.mkdir(input_folder)
        template_path = os.path.join(input_folder, self.config["template"])
        return media_path, template_path

    def creatPDF(self,qrCode_file_path):
        log("start to creat the final tickets")
        output_path, template_path = self.getPath()
        while True:
            print(f"the folder for the ticket template was created: {template_path} copy your template into this folder.")
            input_value = input("Press (y/Y) to continue. ")
            if input_value == "y" or "Y":
                break

        for index, ticket_path in enumerate(qrCode_file_path):
            output_path, template_path = self.getPath(ticket_id=index)
            c = canvas.Canvas('watermark.pdf')
            c.drawImage(ticket_path, self.config["cordsX"], self.config["cordsY"])
            #c.drawImage(ticket_path, 100, 300)
            c.save()
            watermark = PdfFileReader(open("watermark.pdf", "rb"))
            output_file = PdfFileWriter()
            try:
                input_file = PdfFileReader(open(template_path, "rb"))
            except FileNotFoundError as e:
                log(f"{e} \n the standart template will be used now")
                template_path = template_path.replace("template.pdf","standarttemplate.pdf")
                input_file = PdfFileReader(open(template_path, "rb"))
            input_page = input_file.getPage(0)
            input_page.mergePage(watermark.getPage(0))
            output_file.addPage(input_page)
            with open(output_path, "wb") as outputStream:
                output_file.write(outputStream)
            os.remove(ticket_path)
            os.remove("watermark.pdf")
        log("all tickets created!")
