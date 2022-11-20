# extract_doc_info.py
from werkzeug.datastructures import FileStorage
import os
# spacy, ner, hugging face

from utils import PdfField
import os
from enum import Enum
from PyPDF2 import PdfFileReader, PdfFileWriter
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
    return pdf_file_reader != None


def extract_information(pdf_file_reader: PdfFileReader):

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
            if(word == "e-mail:"):
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
    meta_data[PdfField.DEPARTMENT]= ""
    for word in line.split(" , ")[2].split()[2:]:
        meta_data[PdfField.DEPARTMENT] += word
    while(True):
        line_index += 1
        line = sourcefile_lines[line_index]
        if(line.find(",") < 0):
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

def parse_file(file: FileStorage):
    pdfFileReader: Optional[PdfFileReader] = PdfFileReader(file)

    if (not is_pdf(pdfFileReader)):
        print("Given file is not valid pdf file")
        return
    re = extract_information(pdfFileReader)
    print(re)
    return re

def get_configuration(path: str) -> dict:
    with open(path, 'rb') as f:
        return safe_load(f)

def get_signature(file: FileStorage) ->str:
    pdfFileReader = PdfFileReader(file)
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

def strip_values(dict : any):
    for key, value in parsed_data.items():
        parsed_data[key] = value.strip()

def change_pdf_name(old_path:str ,new_path: str) -> str:
    os.rename(old_path, new_path)
    return new_path
if __name__ == '__main__':
    # inputy
    path_to_pdf = 'send_hybrid_gov_01~.pdf'
    path_to_nothing = 'send_hybrid_gov_012~.pdf'
    path_to_config = 'config_algo.yaml'
    yaml_config = get_configuration(path_to_config)
    validator: Validator = Validator(yaml_config)
    
    f = open(path_to_pdf, 'rb')
    pdfFileReader = PdfFileReader(f)
    page = pdfFileReader.getPage(0)
    
    #kod funkcji
    yaml_config = get_configuration(path_to_config)
    validator: Validator = Validator(yaml_config)
    errors = dict
    if (path_to_pdf!=validator.validateName(path_to_pdf)):
        path_to_pdf = change_pdf_name(path_to_pdf,validator.validateName(path_to_pdf))
    parsed_data = parse_file(f)
    parsed_data[PdfField.SIGNATURE] = get_signature(f)
    strip_values(parsed_data)
    
    errors = validator.validateMetaData(parsed_data)

    if(len(errors)==0):
        # return ok
        print("Ok")
    else:
        #return errors(errors)
        print("nie ok")
    # TODO: Stan czy jest error + errors ma być zwracane przez api
