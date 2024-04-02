from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
import docx
import textract
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core. runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter


app = Flask(__name__)
# app.static_folder = "src/templates/static"

# Below function index points to the html template and calls appropriate
# function based on the file type/s that are uploaded.


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            if file.filename.endswith('.pdf'):
                extract_text_from_pdf(file)
            elif file.filename.endswith('.docx'):
                extract_text_from_docx(file)
            elif file.filename.endswith('.txt') or file.filename.endswith('.rtf'):
                extract_text_from_txt_rtf(file)
    return render_template('index.html')


@app.route('/get_files')
def get_files():
    directory = './src/extracted'
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return jsonify(files=files)


@app.route('/generate_rules')
def generate_rules():
    message = "success"
    print("here")
    return jsonify({"message": message})


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    save_text_to_file(text, file.filename)


def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
        save_text_to_file(text, file.filename)


def extract_text_from_txt_rtf(file):
    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join(os.path.dirname(
        __file__), 'temp', file.filename)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    file.save(temp_file_path)

    # Read the temporary file
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Save the extracted text to a file
    save_text_to_file(text, file.filename)

    # Clean up the temporary file
    os.remove(temp_file_path)


def save_text_to_file(text, filename):
    clean_filename = os.path.splitext(filename)[0]
    output_dir = os.path.join(os.path.dirname(__file__), 'extracted')
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f'{clean_filename}.txt')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    print("Hello world")


if __name__ == '__main__':
    app.run(debug=True)
