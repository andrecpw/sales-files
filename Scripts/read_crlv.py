import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
import io
from pdf2image import convert_from_bytes
import re

def create_credentials():
    info = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    }
    credentials = service_account.Credentials.from_service_account_info(info)
    return credentials

def process_crlv(uploaded_file):
    content = None  # Initialize content as None

    if uploaded_file.type == "application/pdf":
        # Convert only the first page of the PDF to an image
        images = convert_from_bytes(uploaded_file.getvalue(), first_page=1, last_page=1)
        if images:  # Check if the list is not empty
            image = images[0]  # Get the first (and only) image
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            content = img_byte_arr.getvalue()
    else:
        # Handle other image types directly
        content = uploaded_file.getvalue()
    return content

def get_crlv_data(content):

    credentials = create_credentials()
    client = vision.ImageAnnotatorClient(credentials=credentials)

    image = vision.Image(content=content)

    # Request for DOCUMENT_TEXT_DETECTION to get structured data
    response = client.document_text_detection(image=image)

        # Keywords to look for, and the variables to store the data
    keywords = {
        "CÓDIGO RENAVAM": "renavam",
        "PLACA": "placa",
        "ANO FABRICAÇÃO": "py",
        "ANO MODELO": "my",
        "CPF / CNPJ": "cpf",
        "MARCA / MODELO / VERSÃO": "marca_modelo",
        "CHASSI": "chassi",  # Special case, data and keyword in different block
        "NOME": "nome",  # Special case, data and keyword in different block
        "COR PREDOMINANTE COMBUSTÍVEL": "cor" # Special case, data and keyword in different block
    }
    # Initialize storage for the data
    data = {key: None for key in keywords.values() if key is not None}
    
    # Temporary variable to store the next expected field
    next_field = None
    vin_regex = r'\b[ABCDEFGHJKLMNPRSTUVWXYZ0-9]{17}\b'  # Regex to match a 17-character VIN

    # Process the response
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # Initialize an empty list to collect paragraphs
            paragraphs_text = []
            for paragraph in block.paragraphs:
                # For each paragraph, join symbols to form words, then join words with spaces
                words_text = ' '.join([''.join([symbol.text for symbol in word.symbols]) for word in paragraph.words])
                paragraphs_text.append(words_text)

                if next_field is not None:
                    # Store the current block considering the last keyword
                    data[next_field] = words_text
                    if next_field == keywords["ANO FABRICAÇÃO"]:
                        next_field = keywords["ANO MODELO"]
                    else:
                        next_field = None 
                elif words_text in keywords:
                    # Store the keyword to store the text of the next block
                    if words_text == "ANO FABRICAÇÃO":
                        next_field = None
                    elif words_text == "ANO MODELO":
                        next_field = keywords["ANO FABRICAÇÃO"]
                    else:
                        next_field = keywords[words_text]
                else:
                    match = re.search(vin_regex, words_text)
                    if match:
                        data['chassi'] = match.group()


            # Join paragraphs with newlines
            block_text = '\n'.join(paragraphs_text)
            
            """print(f"\nBlock confidence: {block.confidence}\n")
            print(f"Block text:\n{block_text}\n")"""

            # Check if the current block contains the specific text
            if "ALIENAÇÃO FIDUCIÁRIA" in block_text:
                # Break out of the loop after printing the desired block
                break

    """for key, value in data.items():
        print(f"{key}: {value}")"""

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))

    return data