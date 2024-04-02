# 9785-24S1-02_RaC

# Rules as Code: Legislation to Business Rules

This project aims to develop a system that can transform traditional government legislation into machine-readable business rules, facilitating efficient service delivery and resource allocation, particularly during times of national disaster.

## Overview

The primary objective of this project is to provide a capability to turn legislation into "Rules as Code" for use as business rules and decision points that could be integrated into current and future systems. By leveraging natural language processing (NLP) techniques and large language models (LLMs), the system can extract key information and conditions from legislation, and translate them into actionable rules.

## Features

- **Legislation Ingestion**: The system can ingest legislation text files and pre-process them for analysis.
- **Natural Language Processing**: Utilizes state-of-the-art NLP models and techniques to analyze and extract relevant information from the legislation text.
- **Business Rule Extraction**: Extracts business rules, conditions, and decision points from the analyzed legislation text.
- **Rules as Code**: Translates the extracted rules into a machine-readable format, YAML, suitable for integration into business rule engines or decision management systems.
- **Scalability**: Designed to handle a diverse range of legislation and accommodate future growth and changes.

## Getting Started

### Prerequisites

- Python 3.7
- ollama server with LLM instruct model
- flask
- textract

### Installation

1. Clone the repository:

  `git clone https://github.com/zetapi/9785-24S1-02_RaC.git`


2. Install the required dependencies:

  `pip install -r requirements.txt`


### Usage
1. Prepare your legislation text file(s) in a compatible format (e.g., plain text).
2. Run the main script, providing the path to your legislation file(s) as an argument:

  `python RaC_proto_.py --input /path/to/legislation/file.txt`

3. The script will analyze the legislation text, extract the business rules, and generate a YAML file containing the rules in a machine-readable format.


## Acknowledgments
- [HuggingFace](https://huggingface.co/) for their open-source NLP models and tools
- [Services Australia](www.servicesaustralia.gov.au/) for being our project sponsor
- [University of Canberra](https://www.canberra.edu.au/) for supporting this capstone project
