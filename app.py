import g4f
from PyPDF2 import PdfReader
import tiktoken 
from flask import Flask, jsonify, request
app = Flask(__name__)

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        pdf_text = ''
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

@app.route('/api', methods=['POST'])
def my_api():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    syllabus_text = pdf_to_text(file)
    token_count = num_tokens_from_string(syllabus_text, "cl100k_base")
    print(f"Number of tokens in syllabus text: {token_count}")
    if token_count > 7900:
        return jsonify({'error': 'Token count exceeded'}), 400

    prompt = f"Given the following college syllabus, extract the relevant dates and events:{syllabus_text} \n Format your response in ics format. "
    response = g4f.ChatCompletion.create(model='gpt-4', messages=[{"role": "user", "content": prompt}], stream=False)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # run the Flask app
