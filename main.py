import g4f
from PyPDF2 import PdfReader
import tiktoken 

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

pdf_path = 'syllabus.pdf'
syllabus_text = pdf_to_text(pdf_path)


token_count = num_tokens_from_string(syllabus_text, "cl100k_base")
print(f"Number of tokens in syllabus text: {token_count}")
if token_count > 7900:
    print("token count exceeded")
    exit()
prompt = f"Given the following college syllabus, extract the relevant dates and events:{syllabus_text} \n Format your response in ics format. "

# streamed completion
response = g4f.ChatCompletion.create(model='gpt-4', messages=[
                                     {"role": "user", "content": prompt}], stream=False)
infile = open("response.ics", 'w')
print(response)
response = '\n'.join(response.split('\n')[1:]).strip()
infile.write(response)
infile.close()
