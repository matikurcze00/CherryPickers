from flask import Flask, request
from flasgger import Swagger
from flasgger import swag_from


app = Flask(__name__)

swagger = Swagger(app=app, template_file='templates/swagger_template.yaml')


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
    return f"{file.filename} uploaded successfully"


if __name__ == '__main__':
    app.run(debug=True)
