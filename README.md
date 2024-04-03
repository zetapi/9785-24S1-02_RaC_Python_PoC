# 9785-24S1-02_RaC

# Rules as Code: Legislation to Business Rules

This project provides a system that can transform traditional government legislation into machine-readable business rules, facilitating efficient service delivery and resource allocation, particularly during times of national disaster.

## Overview

The primary objective of this project was to provide a capability to turn legislation into "Rules as Code" for use as business rules and decision points that could be integrated into current and future systems. By leveraging natural language processing (NLP) techniques and large language models (LLMs), the system can extract key information and conditions from legislation, and translate them into actionable rules.

## Features

- **Simple Web GUI**: The user interface is provided through a webpage that allows for easy selection and conversion of many documents at once.
- **Fast and Portable Deployment**: This program runs within a Docker container and is started with minimal effort.
- **Legislation Ingestion**: The system can ingest legislation text files and pre-process them for analysis.
- **Natural Language Processing**: Utilizes state-of-the-art NLP models and techniques to analyze and extract relevant information from the legislation text.
- **Business Rule Extraction**: Extracts business rules, conditions, and decision points from the analyzed legislation text.
- **Rules as Code**: Translates the extracted rules into a machine-readable format, JSON, suitable for integration into business rule engines or decision management systems.
- **Scalability**: Designed to handle a diverse range of legislation and accommodate future growth and changes.

## Docker image details

### Below is a list of included libraries and packages that the Docker image uses:
- Based around official [Python 3.7 docker image](https://github.com/docker-library/python/)
- [Ollama](https://ollama.com/) server to run LLMs: [mixtral-instruct](https://ollama.com/library/mixtral:8x7b-instruct-v0.1-q5_K_M) and [nomic-embed-text](https://ollama.com/library/nomic-embed-text) models
- [Flask](http://flask.pocoo.org/) for serving the webpage GUI
- Python libs for text extraction and handling: textract, docx, and Py2PDF
- langchain, langchain-community, and langchain-core

## Getting Started

### Prerequisites / Recommended Hardware

- Docker must be installed on the host machine
- Internet access for building the Docker image
- CPU with multiple cores
- ≥ 16 GB RAM
- NVIDIA GPU with CUDA cores, ≥ 8 GB vRAM

### Installation and Setup

1. Clone the repository:

        $ git clone https://github.com/zetapi/9785-24S1-02_RaC_Python_PoC.git

2. Ensure the Docker service is running on the host machine:

        $ sudo systemctl start docker.service

3. Navigate to the cloned repo and build the dockerfile:

        $ cd /path/to/the/repo

        $ docker build -t rac-engine .


### Usage
1. Prepare legislation text file(s) in a compatible format i.e. TXT, RTF, DOCX, and PDF

2. Run the Docker image. This is the image that was built in the previous steps. It will also use the host's network interface, effectively turning it into a server for this app:

        $ docker run --network=host rac-engine

    This container will start the ollama server and start the web server as two separate processes.

3. Open the web page in a browser:
    
    Either: http://localhost:5000/ <br>or http://{host-addr}:5000/

4. Click **"Select Legislation Files"** button and select all pieces of legislation to use as context to provide to the LLM, or just drag-and-drop the files into the indicated section on the page.<br>Once these have been uploaded, the stripped '.txt' versions will appear in the list in the bottom left.

5. Ensure the files that appear in the list are correct, then click **"Generate!"** to start the process of data-embedding.

6. Once embedding is completed, the system will analyze the legislation text, extract the business rules based on a defined schema, and create a JSON file containing the rules in a machine-readable format.

7. Download the JSON file using the **"Download .json"** button. The output file should be named the same as what the main title of the input legislation was, but with a date and time prepended.

    *e.g. 20240415_Farm_Household_Support_Act_2014.json*




## Acknowledgments
- [Ollama](https://ollama.com/) for providing open-source NLP models and tools
- [LangChain]() for tools and libraries to perform data-embedding and retrieval
- Project implementation inspired by [YouTube video](https://www.youtube.com/watch?v=jENqvjpkwmw) by Mervin Praison
- [Services Australia](https://www.servicesaustralia.gov.au/) for being our Project Sponsor
- [University of Canberra Faculty of SciTech](https://www.canberra.edu.au/about-uc/faculties/SciTech/ITS) for supporting this capstone project
