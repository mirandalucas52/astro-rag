import requests

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
