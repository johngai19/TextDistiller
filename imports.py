import fnmatch
import io
import json
import nltk
import os
import re
import shutil
import smtplib
import sys
import torch

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import flash, Flask, render_template, request, redirect, send_file
from flask_socketio import SocketIO
from gingerit.gingerit import GingerIt
from nltk.tokenize import sent_tokenize, word_tokenize
from pdfminer.converter import HTMLConverter, TextConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from threading import Thread
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["PDF_UPLOADS"] = "static/pdf/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["PDF"]
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
