import codecs

from flask import Flask, request
from flasgger import Swagger
from flasgger import swag_from

from PyPDF2 import PdfFileReader

app = Flask(__name__)

swagger = Swagger(app=app, template_file='templates/swagger_template.yaml')


def encode_file_bytes(payload: bytes) -> str:
    return codecs.decode(codecs.encode(payload, 'base64'), 'utf-8')


def decode_file_string(payload: str) -> bytes:
    return codecs.decode(codecs.encode(payload, 'utf-8'), 'base64')


@app.route('/hello_world', methods=['GET'])
@swag_from('templates/hello_world.yaml')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/post_file', methods=['POST'])
@swag_from('templates/post_file.yaml')
def post_file():
    if 'file' not in request.files:
        return "dupa blada"

    file = request.files['file']
    pdf_file = PdfFileReader(file)
    pages = [pdf_file.getPage(page_num) for page_num in range(pdf_file.numPages)]
    print(pages)

    return f"{file.filename} uploaded successfully"


if __name__ == '__main__':
    app.run(debug=True)
