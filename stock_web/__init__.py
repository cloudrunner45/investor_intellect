from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
load_dotenv()  # Loads the .env file
database_url = os.getenv('DATABASE_URL')
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config['SECRET_KEY'] = secret_key
# Initialize SQLAlchemy database
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)  # Bind SQLAlchemy instance to the Flask app





from stock_web import routes