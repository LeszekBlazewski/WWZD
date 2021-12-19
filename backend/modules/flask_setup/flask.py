from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig, ProductionConfig
import os

app = Flask(__name__)
CORS(app)

# load config
if os.getenv("ENV") == "development":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
