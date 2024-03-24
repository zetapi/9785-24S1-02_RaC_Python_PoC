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

def extract_text_from_txt_rtf(file):
    text = textract.process(file, extension=file.filename.split('.')[-1]).decode('utf-8')
    save_text_to_file(text, file.filename)

def save_text_to_file(text, filename):
    clean_filename = os.path.splitext(filename)[0]
    with open(f'extracted/{clean_filename}.txt', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == '__main__':
    app.run(debug=True)
