from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from models import init_db
from controllers import api

app = Flask(__name__)
CORS(app)
Swagger(app)

app.register_blueprint(api)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
