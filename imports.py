import io
import json
import os
import re
import sys
import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from flask import Flask, render_template, request, redirect, send_file
from pdfminer.converter import HTMLConverter, TextConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from werkzeug.utils import secure_filename

