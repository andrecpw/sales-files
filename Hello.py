import streamlit as st
import datetime as dt
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

    st.write("Form Submitted.")
    
    return form_data

# Set page config
st.set_page_config(page_title="Ficha de Vendas", page_icon="📝")

def main():

    st.title('Ficha de Vendas')

    # Use a form for better user experience (submits all at once)
    with st.form(key='sales_form'):
        st.subheader('Cliente:')
        CLIENTE = st.text_input('Nome:')
        CPF = st.text_input('CPF:')
        RG = st.text_input('RG:')
        EXPEDICAO = st.text_input('Expedição:')
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

        st.subheader('Veículo Usado:')
        USADO_VEICULO = st.text_input('Veículo Usado:')
        USADO_VALOR = st.text_input('Valor:')
        USADO_PLACA = st.text_input('Placa do Veículo Usado:')
        USADO_RENAVAM = st.text_input('RENAVAM do Veículo Usado:')
        USADO_CHASSI = st.text_input('Chassi do Veículo Usado:')
        USADO_COR = st.text_input('Cor:')
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
        #TODO figure out the text area size
        NEGOCIACAO = st.text_area('Forma de Pagamento: (Máximo 6 linhas)')

        st.subheader('Observações:')
        OBSERVACAO = st.text_input('Observações:')
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
            'OPCIONAIS': OPCIONAIS,
            'COMBUSTIVEL': COMBUSTIVEL,
            'COR': COR,
            'PY_MY': PY + "/" + MY,
            'CHASSI': CHASSI,
            'PRECO': PRECO,
            'PLACA': PLACA,

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

        template_pdf_path = "Templates\NOVA Ficha de Vendas V4 (FORM).pdf"
        filled_pdf_path = f"Output/FV_{form_data['name']}.pdf"
        fill_pdf(template_pdf_path, filled_pdf_path, form_data)

        # Create a link to download the PDF
        with open(filled_pdf_path, "rb") as file:
            st.download_button(
                label="Download Ficha de Vendas",
                data=file,
                file_name=f"FV_{form_data['name']}.pdf",
                mime="application/octet-stream"
            )

if __name__ == "__main__":
    main()