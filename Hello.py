import streamlit as st
import datetime as dt
import tempfile
import zipfile
import os
from Scripts.pdf_generator import fill_pdf

# Function to process the form data (this is where you would add your PDF filling logic)
def process_form_data(form_data):
    # You can process and save the data, or generate a PDF using a library like PyPDF2 or reportlab
    if form_data["EMPLACAMENTO_PGTO"] == "Loja":
        form_data["EMPLACAMENTO_LOJA"] = "X"
    elif form_data["EMPLACAMENTO_PGTO"] == "Cliente":
        form_data["EMPLACAMENTO_CLIENTE"] = "X"

    if form_data["IPVA_PGTO"] == "Loja":
        form_data["IPVA_LOJA"] = "X"
    elif form_data["IPVA_PGTO"] == "Cliente":
        form_data["IPVA_CLIENTE"] = "X"

    if form_data["ESCOLHA_PLACA_PGTO"] == "Loja":
        form_data["ESCOLHA_PLACA_LOJA"] = "X"
    elif form_data["ESCOLHA_PLACA_PGTO"] == "Cliente":
        form_data["ESCOLHA_PLACA_CLIENTE"] = "X"

    if form_data["OUTROS_PGTO"] == "Loja":
        form_data["OUTROS_LOJA"] = "X"
    elif form_data["OUTROS_PGTO"] == "Cliente":
        form_data["OUTROS_CLIENTE"] = "X"

    if form_data.get("AUTORIZACAO_AUTORIZADO", "") != "":
        form_data["AUTORIZACAO_CLIENTE"] = form_data["CLIENTE"]

    # Process the NEGOCIACAO field
    negociacao_parts = form_data.get("NEGOCIACAO", "").split('\n')
    for i in range(1, 7):
        form_data[f"NEGOCIACAO_{i}"] = negociacao_parts[i - 1] if i <= len(negociacao_parts) else ""

    # Convert all string values to uppercase
    form_data = {key: value.upper() if isinstance(value, str) else value for key, value in form_data.items()}

    # Process CPF and CNPJ
    number = form_data.get(CPF, None)
    if number:
        if len(number) == 11:  # CPF
            form_data["PESSOA_FISICA"] = "S"
            return f"{number[:3]}.{number[3:6]}.{number[6:9]}-{number[9:]}"
        elif len(number) == 14:  # CNPJ
            form_data["PESSOA_FISICA"] = "N"
            return f"{number[:2]}.{number[2:5]}.{number[5:8]}/{number[8:12]}-{number[12:]}"

    st.write("Form Submitted.")
    
    return form_data

# Function to create a PDF and return its path with a custom name
def create_pdf_and_return_path(template_path, form_data, prefix):
    # Create a temporary file with a custom name
    fd, path = tempfile.mkstemp(suffix=".pdf", prefix=f"{prefix}_{form_data['CLIENTE']}_")
    os.close(fd)  # Close the file descriptor

    # Fill the PDF with data
    fill_pdf(template_path, path, form_data)
    return path

# Set page config
st.set_page_config(page_title="Ficha de Vendas", page_icon="📝")

def main():

    st.title('Ficha de Vendas')

    # Use a form for better user experience (submits all at once)
    with st.form(key='sales_form'):
        st.subheader('Cliente:')
        CLIENTE = st.text_input('Nome:')
        CPF = st.text_input('CPF/CNPJ (Somente números):')
        RG = st.text_input('RG:')
        DATA_NASCIMENTO = st.date_input(
            label='Data de Nascimento:',
            min_value=dt.date(1920, 1, 1),
            format=("DD/MM/YYYY")
        )
        CELULAR = st.text_input('Celular:')
        FONE = st.text_input('Telefone:')
        RUA = st.text_input('Rua:')
        NUMERO = st.text_input('Número:')
        BAIRRO = st.text_input('Bairro:')
        CIDADE = st.text_input('Cidade:')
        ESTADO = st.text_input('Estado:')
        CEP = st.text_input('CEP:')
        EMAIL = st.text_input('Email:')

        st.subheader('Negociação:')
        MARCA = st.text_input('Marca:')
        MODELO = st.text_input('Modelo:')
        OPCIONAIS = st.text_input('Opcionais:')
        COMBUSTIVEL = st.text_input('Combustível:')
        COR = st.text_input('Cor:')
        PY = st.text_input('Ano de Produção:')
        MY = st.text_input('Ano do Modelo:')
        CHASSI = st.text_input('Chassi:')
        PRECO = st.text_input('Preço:')
        PLACA = st.text_input('Placa:')
        RENAVAM = st.text_input('RENAVAM:')

        st.subheader('Veículo Usado:')
        USADO_VEICULO = st.text_input('Veículo Usado:')
        USADO_VALOR = st.text_input('Valor:')
        USADO_PLACA = st.text_input('Placa do Veículo Usado:')
        USADO_RENAVAM = st.text_input('RENAVAM do Veículo Usado:')
        USADO_CHASSI = st.text_input('Chassi do Veículo Usado:')
        USADO_COR = st.text_input('Cor:', key='usado_cor')
        USADO_PY = st.text_input('Ano Produção:')
        USADO_MY = st.text_input('Ano Modelo:')
        USADO_KM = st.text_input('KM do Veículo Usado:')
        USADO_QUITACAO = st.text_input('Quitação:')

        st.subheader('Forma de Pagamento:')
        NF = st.text_input('Valor Nota Fiscal:')
        FINANCIAMENTO = st.text_input('Valor Financiado:')
        BANCO = st.text_input('Banco:')
        N_PARCELAS = st.text_input('Número de Parcelas:')
        VALOR_PARCELA = st.text_input('Valor Parcela')
        NEGOCIACAO = st.text_area('Forma de Pagamento: (Máximo 6 linhas)')
        OBSERVACAO = st.text_input('Observações (Cortesias):')

        st.subheader('Retirada:')
        AUTORIZACAO = st.checkbox('Outra pessoa irá retirar o veículo')
        AUTORIZACAO_AUTORIZADO = st.text_input('Nome da pessoa:')

        st.subheader('Serviços:')
        free = 'Loja'
        cust = 'Cliente'
        EMPLACAMENTO_PGTO = st.radio('Emplacamento/Transferência', [cust, free], horizontal=True)
        IPVA_PGTO = st.radio('IPVA', [cust, free], horizontal=True)
        ESCOLHA_PLACA_PGTO = st.radio('Escolha de Placa', ['Não', cust, free], horizontal=True)
        ESCOLHA_PLACA = st.text_input('Observação Escolha de Placa:')
        OUTROS = st.text_input('Outros:')
        OUTROS_PGTO = st.radio('Outros', ['Não', cust, free], horizontal=True)

        # Form submit button
        submit_button = st.form_submit_button(label='Submit')

    # Process the form data when the button is pressed
    if submit_button:
        form_data = {
            'CLIENTE': CLIENTE,
            'CPF': CPF,
            'RG': RG,
            'DATA_NASCIMENTO': str(DATA_NASCIMENTO),
            'FONE': FONE,
            'CELULAR': CELULAR,
            'RUA': RUA,
            'NUMERO': NUMERO,
            'ENDERECO': RUA + ", " + NUMERO,
            'BAIRRO': BAIRRO,
            'CIDADE': CIDADE,
            'ESTADO': ESTADO,
            'CEP': CEP,
            'EMAIL': EMAIL,

            'MARCA': MARCA,
            'MODELO': MODELO,
            'VEICULO': MARCA + " / " + MODELO,
            'OPCIONAIS': OPCIONAIS,
            'COMBUSTIVEL': COMBUSTIVEL,
            'COR': COR,
            'PY_MY': PY + "/" + MY,
            'CHASSI': CHASSI,
            'PRECO': PRECO,
            'PLACA': PLACA,
            'RENAVAM': RENAVAM,

            'USADO_VEICULO': USADO_VEICULO,
            'USADO_VALOR': USADO_VALOR,
            'USADO_PLACA': USADO_PLACA,
            'USADO_RENAVAM': USADO_RENAVAM,
            'USADO_CHASSI': USADO_CHASSI,
            'USADO_COR': USADO_COR,
            'USADO_PY': USADO_PY,
            'USADO_MY': USADO_MY,
            'USADO_PY_MY': USADO_PY + "/" + USADO_MY,
            'USADO_KM': USADO_KM,
            'USADO_QUITACAO': USADO_QUITACAO,

            'NF': NF,
            'FINANCIAMENTO': FINANCIAMENTO,
            'BANCO': BANCO,
            'N_PARCELAS': N_PARCELAS,
            'VALOR_PARCELA': VALOR_PARCELA,
            'NEGOCIACAO': NEGOCIACAO,
            'OBSERVACAO': OBSERVACAO,
            'AUTORIZACAO': AUTORIZACAO,
            'AUTORIZACAO_AUTORIZADO': AUTORIZACAO_AUTORIZADO,
            'EMPLACAMENTO_PGTO': EMPLACAMENTO_PGTO,
            'IPVA_PGTO': IPVA_PGTO,
            'ESCOLHA_PLACA_PGTO': ESCOLHA_PLACA_PGTO,
            'ESCOLHA_PLACA': ESCOLHA_PLACA,
            'OUTROS': OUTROS,
            'OUTROS_PGTO': OUTROS_PGTO
        }

        form_data = process_form_data(form_data)

        pdf_paths = []

        # Always fill the primary PDF template
        pdf_paths.append(create_pdf_and_return_path("Templates/NOVA Ficha de Vendas V4.pdf", form_data, "FV"))

        # Fill Procuração de Comprador based on CPF length
        if form_data.get("PLACA", "") != "":
            if form_data.get("PESSOA_FISICA", "") == "S":
                pdf_paths.append(create_pdf_and_return_path("Templates/PROCURAÇÃO DE COMPRADOR PF.pdf", form_data, "Proc"))
            elif form_data.get("PESSOA_FISICA", "") == "N":
                pdf_paths.append(create_pdf_and_return_path("Templates/PROCURAÇÃO DE COMPRADOR PJ.pdf", form_data, "Proc"))

        # Fill Termo de Multas based on CPF length
        if form_data.get("USADO_VEICULO", "") != "":
            if form_data.get("PESSOA_FISICA", "") == "S":
                pdf_paths.append(create_pdf_and_return_path("Templates/Termo de Multas - PF.pdf", form_data, "TM"))
            elif form_data.get("PESSOA_FISICA", "") == "N":
                pdf_paths.append(create_pdf_and_return_path("Templates/Termo de Multas - PJ.pdf", form_data, "TM"))

        # Create a ZIP file from the generated PDFs
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmpzip:
            with zipfile.ZipFile(tmpzip.name, 'w') as zipf:
                for pdf in pdf_paths:
                    zipf.write(pdf, os.path.basename(pdf))
                    os.remove(pdf)  # Remove the PDF file after adding it to the ZIP

            # Provide a download button for the ZIP file
            with open(tmpzip.name, "rb") as file:
                st.download_button(
                    label="Download PDFs as ZIP",
                    data=file,
                    file_name="filled_forms.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()