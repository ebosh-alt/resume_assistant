import datetime
import logging
import os
import time
import zipfile
from xml.etree import ElementTree
import docx2txt
import pdfplumber
from os import listdir
from os.path import isfile, join
from spire.doc import Document, FileFormat

from data.config import BASE_PATH_PDF

logger = logging.getLogger(__name__)


class CheckFile:
    def len(self, path_file: str):
        type_file = path_file.split(".")[-1]
        match type_file:
            case "docx":
                return self.len_docx(path_file)
            case "pdf":
                return self.len_pdf(path_file)
            case "txt":
                return self.len_txt(path_file)
            case "doc":
                return self.len_doc(path_file)
            case _:
                raise ValueError(f"Invalid path_file: {path_file}")

    @staticmethod
    def len_docx(path_file):
        total = 0
        zin = zipfile.ZipFile(path_file)
        for item in zin.infolist():
            if item.filename == 'docProps/app.xml':
                buffer = zin.read(item.filename)
                root = ElementTree.fromstring(buffer.decode('utf-8'))
                for child in root:
                    if child.tag.endswith('Characters'):
                        total += int(child.text)
        return total

    @staticmethod
    def len_pdf(path_file):
        with pdfplumber.open(path_file) as pdf:
            total = 0
            for page in pdf.pages:
                for ind in range(len(page.chars)):
                    symbol = page.chars[ind]["text"]
                    if symbol == " " or symbol == "\n":
                        continue
                    total += 1
        return total

    @staticmethod
    def len_txt(path_file):
        with open(path_file, "r", encoding="utf-8") as f:
            text = f.read().replace(" ", "").replace("\n", "")
        return len(text)

    @staticmethod
    def convert_doc_to_docx(path_file):
        document = Document()
        document.LoadFromFile(path_file)
        document.SaveToFile(f"{path_file[:len(path_file) - 4]}.docx", FileFormat.Docx2016)
        document.Close()

    @staticmethod
    def delete_files():
        while True:
            now = datetime.datetime.now()
            if now.hour == 0:
                all_files = [f for f in listdir(BASE_PATH_PDF) if isfile(join(BASE_PATH_PDF, f))]
                for file in all_files:
                    path_file = BASE_PATH_PDF + '/' + file
                    os.remove(path_file)
                logger.info("Delete files: %s" % ",".join(all_files))
            time.sleep(1 * 60 * 45)
