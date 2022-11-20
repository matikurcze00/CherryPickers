# extract_doc_info.py

from PyPDF2 import PdfFileReader
from PyPDF2.errors import PdfReadError
from typing import Optional

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
            if(word == "e-mail:"):
                index = word.find("e-mail")
                meta_data["Nadawca e-mail"] = line.split()[index + 1]
                meta_data["Nadawca ePUAP"] = line.split()[index + 4]

                line_index = sourcefile_lines.index(line)
                break
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data["Nadawca Nazwa"] = line.split(" ,")[0]
    meta_data["Nadawca Ulica"] = line.split(" ,")[1]
    meta_data["Nadawca Kod Pocztowy"] = line.split(" , ")[2].split()[0]
    meta_data["Nadawca Miasto"] = line.split(" , ")[2].split()[1]
    meta_data["Urzad"]= ""
    for word in line.split(" , ")[2].split()[2:]:
        meta_data["Urzad"] += word
    while(True):
        line_index += 1
        line = sourcefile_lines[line_index]
        if(line.find(",")<0):
            meta_data["Urzad"] += line
        else:
            break

    meta_data["UNP"] = ""
    while(True):
        line_index += 1
        line = sourcefile_lines[line_index]
        if(line.find("UNP:")>=0):
            for word in line[line.find("UNP:")+4:]:
                meta_data["UNP"] += word 
            break 
    line_index += 1
    line = sourcefile_lines[line_index]
    if(line.find("Sprawa:")>=0):
        meta_data["Sprawa"] = ""
        for word in line[line.find("Sprawa:")+7:]:
                meta_data["Sprawa"] += word 
        line_index += 1
    while(True):
        if(line.strip()==""):
            line_index += 1
            break
        line_index += 1
        line = sourcefile_lines[line_index]
    meta_data["Odbiorca nazwa"] = line
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data["Odbiorca ulica"] = line
    line_index += 1
    line = sourcefile_lines[line_index]
    meta_data["Odbiorca kod pocztowy"] = line.split()[0]
    meta_data["Odbiorca miasto"] = ""
    for word in line.split()[1:]:
        meta_data["Odbiorca miasto"]+=word


    print(meta_data) 

def parse_file(path: str) -> None:
    pdfFileReader: Optional[PdfFileReader] = open_file(path)

    if (not is_pdf(pdfFileReader)):
        print("Given file is not valid pdf file")
        return
    
    extract_information(pdfFileReader)

if __name__ == '__main__':
    path_to_pdf = 'send_hybrid_gov_01~.pdf'
    path_to_nothing = 'send_hybrid_gov_012~.pdf'
    f = open(path_to_pdf, 'rb')
    pdfFileReader = PdfFileReader(f)
    page = pdfFileReader.getPage(0)
    parse_file(path_to_pdf)
    # parse_file(path_to_nothing) #Nie dziala dla zlego pliku