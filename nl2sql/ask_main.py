import sqlite3
import os
import sys
import time
from google import genai
from google.genai import types
from google.genai import errors
from dotenv import load_dotenv
from tabulate import tabulate

def get_schema(db_path):
    print('1')
def generate_sql(client, question, schema, last_sql=None, last_error=None):
    print('2')


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

