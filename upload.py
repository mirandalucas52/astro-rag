import requests
import PyPDF2

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
                text += page.extract_text() + " "
            print("Text extracted:", text)