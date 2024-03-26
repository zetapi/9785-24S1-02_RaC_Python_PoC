from flask import Flask, render_template, request
import os
import PyPDF2
import docx
import textract


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
       print("Hello, I'm here")
       files = request.files.getlist('files')
       for file in files:
           if file.filename.endswith('.pdf'):
               extract_text_from_pdf(file)
           elif file.filename.endswith('.docx'):
               extract_text_from_docx(file)
           elif file.filename.endswith('.txt') or file.filename.endswith('.rtf'):
               extract_text_from_txt_rtf(file)
   return render_template('index.html')


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


def extract_text_from_txt_rtf(file_storage):
    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join(os.path.dirname(__file__), 'temp', file_storage.filename)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    file_storage.save(temp_file_path)

    # Read the temporary file
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Save the extracted text to a file
    save_text_to_file(text, file_storage.filename)

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
