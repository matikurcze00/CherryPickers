# extract_doc_info.py
from werkzeug.datastructures import FileStorage
import os
# spacy, ner, hugging face

from utils import PdfField

from enum import Enum
from PyPDF2 import PdfFileReader
from PyPDF2.errors import PdfReadError
from typing import Optional
from validation import Validator
from yaml import safe_load


def get_pdf_text_from_page(pdf_file_reader: PdfFileReader, page_number: int) -> str:
    page = pdf_file_reader.getPage(page_number)

    return page.extractText()


def open_file(pdf_path: str) -> Optional[PdfFileReader]:
    try:
        f = open(pdf_path, 'rb')
        pdfFileReader = PdfFileReader(f)
        return pdfFileReader
    except PdfReadError as e:
        return None


def is_pdf(pdf_file_reader: Optional[PdfFileReader]) -> bool:
    return pdf_file_reader is not None


def extract_information(pdf_file_reader: PdfFileReader):
    print(type(pdf_file_reader))

    START_PAGE = 0
    text = get_pdf_text_from_page(pdf_file_reader, START_PAGE)
    number_of_pages = pdf_file_reader.getNumPages()
    file_information = pdf_file_reader.getDocumentInfo()

    sourcefile_lines = []
    line_index = 0
    meta_data = {}

    for line in text.splitlines():
        sourcefile_lines.append(line)
    for line in sourcefile_lines:
        for word in line.split(" "):
            if word == "e-mail:":
                index = word.find("e-mail")
                meta_data[PdfField.SENDER_EMAIL] = line.split()[index + 1]
                meta_data[PdfField.SENDER_EPUAP] = line.split()[index + 4]

                line_index = sourcefile_lines.index(line)
                break
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data[PdfField.SENDER_NAME] = line.split(" ,")[0]
    meta_data[PdfField.SENDER_STREET] = line.split(" ,")[1]
    meta_data[PdfField.SENDER_ZIP_CODE] = line.split(" , ")[2].split()[0]
    meta_data[PdfField.SENDER_CITY] = line.split(" , ")[2].split()[1]
    meta_data[PdfField.DEPARTMENT] = ""
    for word in line.split(" , ")[2].split()[2:]:
        meta_data[PdfField.DEPARTMENT] += word
    while True:
        line_index += 1
        line = sourcefile_lines[line_index]
        if line.find(",") < 0:
            meta_data[PdfField.DEPARTMENT] += line
        else:
            break
    meta_data[PdfField.DATE] = line.split(",")[1]
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data[PdfField.UNP] = ""
    while(True):
        if(line.find("UNP:")>=0):
            for word in line[line.find("UNP:") + 4:]:
                meta_data[PdfField.UNP] += word 
            line_index += 1
            line = sourcefile_lines[line_index]
            break 
        line_index += 1
        line = sourcefile_lines[line_index]

    if(line.find("Sprawa:")>=0):
        meta_data[PdfField.CASE_TYPE] = ""
        for word in line[line.find("Sprawa:") + 7:]:
                meta_data[PdfField.CASE_TYPE] += word 
        line_index += 1
        line = sourcefile_lines[line_index]

    while(True):
        if(line.strip()==""):
            line_index += 1
            break
        line_index += 1
        line = sourcefile_lines[line_index]
    meta_data[PdfField.RECEIVER_NAME] = line
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data[PdfField.RECEIVER_STREET] = line
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data[PdfField.RECEIVER_ZIP_CODE] = line.split()[0]
    meta_data[PdfField.RECEIVER_CITY] = ""
    for word in line.split()[1:]:
        meta_data[PdfField.RECEIVER_CITY] += word

    return meta_data 



def parse_file(file: FileStorage) -> None:
    # pdfFileReader: Optional[PdfFileReader] = PdfFileReader(file)

    if not is_pdf(pdfFileReader):
        print("Given file is not valid pdf file")
        return

    return extract_information(pdfFileReader)


def get_configuration(path: str) -> dict:
    with open(path, 'rb') as f:
        return safe_load(f)

def get_signature(path: str) ->str:
    f = open(path, 'rb')
    pdfFileReader = PdfFileReader(f)
    text = pdfFileReader.getPage(pdfFileReader.numPages-1).extract_text()
    sourcefile_lines = []
    for ind, line in enumerate(text.splitlines()):
        if(line.find("(podpisano kwalifikowanym podpisem elektronicznym)")>=0 or
         (line.find("(podpisano kwalifikowanym")>=0 and text.splitlines()[ind+1].find("podpisem elektronicznym)")>=0)):
            return sourcefile_lines.pop()
        sourcefile_lines.append(line)
    return ""

def strip_values(dict : any):
    for key, value in parsed_data.items():
        parsed_data[key] = value.strip()

def change_pdf_name(old_path:str ,new_path: str) -> str:
    os.rename(old_path, new_path)
    return new_path

if __name__ == '__main__':
    path_to_pdf = 'send_hybrid_gov_01~.pdf'
    path_to_nothing = 'send_hybrid_gov_012~.pdf'
    path_to_config = 'config_algo.yaml'
    yaml_config = get_configuration(path_to_config)
    validator: Validator = Validator(yaml_config)
    
    f = open(path_to_pdf, 'rb')
    pdfFileReader = PdfFileReader(f)
    page = pdfFileReader.getPage(0)
    parsed_data = parse_file(pdfFileReader)
    parsed_data[PdfField.SIGNATURE] = get_signature(path_to_pdf)
    print(parsed_data)

    
    errors = validator.validate(parsed_data)
    # TODO: errors ma być zwracane przez api
