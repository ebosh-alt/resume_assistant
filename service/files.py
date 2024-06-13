import datetime
import logging
import os
import time
import zipfile
from xml.etree import ElementTree

import pdfplumber
from multiprocessing import Process
from os import listdir
from os.path import isfile, join

from data.config import BASE_PATH_PDF

logger = logging.getLogger(__name__)


class BG:
    def __init__(self, ta) -> None:
        self.process = Process()
        self.pid = self.process.pid


class CheckFile:
    def len(self, path: str):
        type_file = path.split(".")[-1]
        match type_file:
            case "docx":
                return self.len_docx(path)
            case "pdf":
                return self.len_pdf(path)
            case "txt":
                return self.len_txt(path)
            case _:
                raise ValueError(f"Invalid path: {path}")

    @staticmethod
    def len_docx(path):
        total = 0
        zin = zipfile.ZipFile(path)
        for item in zin.infolist():
            if item.filename == 'docProps/app.xml':
                buffer = zin.read(item.filename)
                root = ElementTree.fromstring(buffer.decode('utf-8'))
                for child in root:
                    if child.tag.endswith('Characters'):
                        total += int(child.text)
        return total

    @staticmethod
    def len_pdf(path):
        with pdfplumber.open(path) as pdf:
            total = 0
            for page in pdf.pages:
                for ind in range(len(page.chars)):
                    symbol = page.chars[ind]["text"]
                    if symbol == " " or symbol == "\n":
                        continue
                    total += 1
        return total

    @staticmethod
    def len_txt(path):
        total = 0
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
            for symbol in data:
                if symbol == " " or symbol == "\n":
                    continue
                total += 1
        return total

    @staticmethod
    def delete_files():
        while True:
            now = datetime.datetime.now()
            if now.hour == 0:
                all_files = [f for f in listdir(BASE_PATH_PDF) if isfile(join(BASE_PATH_PDF, f))]
                for file in all_files:
                    path = BASE_PATH_PDF + '/' + file
                    os.remove(path)
                logger.info("Delete files: %s" % ",".join(all_files))
            time.sleep(1 * 60 * 45)
