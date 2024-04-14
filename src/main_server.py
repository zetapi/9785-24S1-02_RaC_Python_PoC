from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
import docx
import textract
import requests
import json
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TextSplitter


app = Flask(__name__)

retriever = Chroma()

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
    print("Starting rules generation procedure")
    # Starts the full text embedding and rules generation
    rag_rules_gen_chain()

    # Returns status to the web app for showing the buttons
    return jsonify({"message": message})


def get_model_name():
    """
    Reads the model name from the ./config/model.txt file.
    """
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    model_file = os.path.join(config_dir, 'model')
    
    try:
        with open(model_file, 'r') as f:
            model_name = f.read().strip()
        print(f"Model successfully set: {model_name}")
        return model_name
    except FileNotFoundError:
        print(f"Error: {model_file} not found.")
        print("Setting to default model: tinydolphin...")
        download_tinydolphin()
        model_name = "tinydolphin:1.1b-v2.8-q2_K"
        return model_name
    except Exception as e:
        print(f"Error reading {model_file}: {e}")
        print("Setting to default model: tinydolphin...")
        download_tinydolphin()
        model_name = "tinydolphin:1.1b-v2.8-q2_K"
        return model_name


def get_instructions():
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    inst_file = os.path.join(config_dir, 'instructions')
    try:
        with open(inst_file, 'r') as f:
            instructions = f.read().strip()
        return instructions
    except FileNotFoundError:
        print(f"Error: {inst_file} file not found.")
        return "Write a very short story about a beekeeper with an itchy nose"


def download_tinydolphin():
    url = "http://localhost:11434/api/pull"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "name": "tinydolphin:1.1b-v2.8-q2_K"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        # data = json.loads(response_text)
        # actual_response = data["response"]
        print(response_text)
    else:
        print("Error:", response.status_code, response.text)


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


def rag_rules_gen_chain():
    rag_template = """Follow the instructions based only on the following context:
    {context}
    Instruction: {instructions}
    """
    rag_prompt = ChatPromptTemplate.from_template(rag_template)
    
    rag_chain = (
        {"context": embedding_retrieval(), "instructions": RunnablePassthrough()}
        | rag_prompt
        | model_local
        | StrOutputParser()
    )

    # print(rag_chain.invoke(get_instructions()))

    if not os.path.exists('./src/output/'):
        print("Initialising output directory: ./src/output/")
        os.mkdir('./src/output/')

    with open('./src/output/out.json', 'w') as writer:
        print("Writing output file: out.json")
        for s in rag_chain.stream(get_instructions()):
            print(s)
            writer.write(s)


    # model_local = Ollama(model=get_model_name())


    # print(f"ChromaDB retriever created\n")
    # print(f"###\nTest joke:")
    # rag_template = "Tell me a funny joke about {topic}"
    # rag_prompt = ChatPromptTemplate.from_template(rag_template)
    # rag_chain = rag_prompt | model_local | StrOutputParser()
    # print(rag_chain.invoke({"topic": "bees"}))
    


    # print ("\n########\nAfter RAG\n")
    # after_rag_template = """Answer the question based only on the following context:
    # {context}
    # Question: {question}
    # """
    # after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    # after_rag_chain = (
    #     {"context": retriever, "question": RunnablePassthrough()}
    #     | after_rag_prompt
    #     | model_local
    #     | StrOutputParser()
    # )
    # print (after_rag_chain.invoke("What is Ollama?"))

def embedding_retrieval():
    # Grab all extracted documents to be processed
    directory = './src/extracted'
    loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()
    print(f"Loaded {len(docs)} extracted doc/s")
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs)
    print(f"Split {len(doc_splits)}")

    retriever = (Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')
    )).as_retriever()
    print(f"ChromaDB retriever created\n")
    return retriever


def main():
    print("Hello world")


if __name__ == '__main__':
    model_local = Ollama(model=get_model_name())
    app.run(debug=True, host='0.0.0.0', port=5000)
    # , host='0.0.0.0', port=5000
