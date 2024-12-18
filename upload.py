import requests
import PyPDF2
import re

def convert_pdf_to_text():
    file_id = "1-lEpAcgZ7B05yVJUK4OJyEdB9t7x031i"
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    if response.status_code == 200:
        with open("output.pdf", "wb") as f:
            f.write(response.content)
        print("File downloaded successfully!")
    else:
        print("Failed to download the file. Status code:", response.status_code)
    
    file_path = "output.pdf"
    if file_path:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            if not text:
                print("No text extracted from the PDF.")
            else:
                print("Text extracted:", text)
                
            text = re.sub(r'\s+', ' ', text).strip()
            
            sentences = re.split(r'(?<=\.)\s+(?=[A-Za-z])', text)
            
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)

            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n") 
            print(f"PDF content appended to vault.txt with each chunk on a separate line.")

convert_pdf_to_text()