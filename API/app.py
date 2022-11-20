import codecs
from uuid import uuid4

from config import cf, cf_algo
from validation import Validator

from flask import Flask, request, send_file, redirect
from flask_cors import CORS
from flasgger import Swagger
from flasgger import swag_from
from PyPDF2 import PdfFileReader, PdfWriter

app = Flask(__name__)
CORS(app)

swagger = Swagger(app=app, template_file='templates/swagger_template.yaml')


def encode_file_bytes(payload: bytes) -> str:
    return codecs.decode(codecs.encode(payload, 'base64'), 'utf-8')


def decode_file_string(payload: str) -> bytes:
    return codecs.decode(codecs.encode(payload, 'utf-8'), 'base64')


@app.route('/', methods=['GET'])
def apidocs():  # put application's code here
    return redirect('/apidocs')


@app.route('/hello_hackyeah', methods=['GET'])
@swag_from('templates/hello_world.yaml')
def hello_world():  # put application's code here
    return 'Hello HackYeah!!!'


@app.route('/file', methods=['POST'])
@swag_from('templates/post_file.yaml')
def post_file():
    if 'file' not in request.files:
        return "Request missing required field or malformed", 400

    file = request.files['file']

    valid = Validator(cf_algo.to_dict())
    errors_dict = valid.validate(parsed_dict={})

    pdf_file = PdfFileReader(file)
    pages = [pdf_file.getPage(page_num) for page_num in range(pdf_file.numPages)]
    writer = PdfWriter()
    [writer.add_page(page) for page in pages]

    uuid = uuid4()
    with open(f"pdfs/{uuid}.pdf", "wb") as f:
        writer.write(f)

    return {
        "info": f"{file.filename} uploaded successfully",
        "uuid": f"{str(uuid)}",
        "errors": errors_dict
    }


@app.route('/file/<string:uuid>', methods=['GET'])
@swag_from('templates/get_file.yaml')
def get_file(uuid: str):
    return send_file(f"pdfs/{uuid}.pdf", mimetype="pdf", as_attachment=True)


@app.route('/config_algo', methods=['GET'])
@swag_from('templates/get_config_algo.yaml')
def get_config_algo():
    return cf_algo.to_dict()


@app.route('/config_algo', methods=['POST'])
@swag_from('templates/post_config_algo.yaml')
def post_config_algo():
    try:
        data = request.get_json()
        cf_algo.update(config_dict=data["config_dict"])
        return cf_algo.to_dict(), 200
    except Exception as e:
        return f"fail to update config. Error: {str(e)}", 500


def run_api(debug: bool, path_to_config: str, path_to_algo_config):
    cf.load_config(path_to_config)
    cf_algo.load_config(path_to_algo_config)
    app.run(debug=debug, host=cf.ip_address, port=cf.port)


if __name__ == '__main__':
    app.run(debug=True)
