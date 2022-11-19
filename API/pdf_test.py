from PyPDF2 import PdfFileReader

pdfFileObj = open('sample.pdf', 'rb')

pdfReader = PdfFileReader(pdfFileObj)


if __name__ == '__main__':
    print(pdfReader.numPages)
    pages = [pdfReader.getPage(page_num) for page_num in range(pdfReader.numPages)]
    print(pages)
    pages[0]