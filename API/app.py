import codecs
from uuid import uuid4

from werkzeug.datastructures import FileStorage

from config import cf, cf_algo

from flask import Flask, request, send_file, redirect
from flask_cors import CORS
from flasgger import Swagger
from flasgger import swag_from
from PyPDF2 import PdfFileReader, PdfWriter
from docx2pdf import convert

app = Flask(__name__)
CORS(app)

swagger = Swagger(app=app, template_file='templates/swagger_template.yaml')


def encode_file_bytes(payload: bytes) -> str:
    return codecs.decode(codecs.encode(payload, 'base64'), 'utf-8')


def decode_file_string(payload: str) -> bytes:
    return codecs.decode(codecs.encode(payload, 'utf-8'), 'base64')


def covert_file_if_not_pdf(file: FileStorage) -> FileStorage:
    if file.filename.endswith(".pdf"):
        return file
    elif file.filename.endswith(".docx"):
        return convert(file)


@app.route('/', methods=['GET'])
def apidocs():  # put application's code here
    return redirect('/apidocs')


@app.route('/hello_world', methods=['GET'])
@swag_from('templates/hello_world.yaml')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/file', methods=['POST'])
@swag_from('templates/post_file.yaml')
def post_file():
    if 'file' not in request.files:
        return "Request missing required field or malformed", 400

    file = request.files['file']
    pdf_file = PdfFileReader(file)
    pages = [pdf_file.getPage(page_num) for page_num in range(pdf_file.numPages)]

    uuid = uuid4()
    writer = PdfWriter()

    [writer.add_page(page) for page in pages]

    with open(f"pdfs/{uuid}.pdf", "wb") as f:
        writer.write(f)

    return {
        "info": f"{file.filename} uploaded successfully",
        "uuid": f"{str(uuid)}"
    }


@app.route('/file/<string:uuid>', methods=['GET'])
@swag_from('templates/get_file.yaml')
def get_file(uuid: str):
    return send_file(f"pdfs/{uuid}.pdf", mimetype="pdf", as_attachment=True)


@app.route('/config_algo', methods=['GET'])
@swag_from('templates/get_config_algo.yaml')
def get_config_algo():
    return cf_algo.to_dict()


def run_api(debug: bool, path_to_config: str, path_to_algo_config):
    cf.load_config(path_to_config)
    cf_algo.load_config(path_to_algo_config)
    app.run(debug=debug, host=cf.ip_address, port=cf.port)


if __name__ == '__main__':
    app.run(debug=True)
