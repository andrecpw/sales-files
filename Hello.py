import streamlit as st
import datetime as dt
import tempfile
import zipfile
import os
from Scripts.pdf_generator import create_pdf_and_return_path
from Scripts.data_processing import process_form_data, process_other_proprietor, process_cpf
from Scripts.read_crlv import process_crlv, get_crlv_data
from Scripts.notion_handler import initialize_notion_client, add_form_data_to_notion


# Set page config
st.set_page_config(page_title="Ficha de Vendas Teste", page_icon="📝")

def main():

    st.title('Ficha de Vendas')

    # Initialize session state variables for used vehicle fields if not already present
    fields = [
        'usado_marca', 'usado_modelo', 'usado_placa', 
        'usado_renavam', 'usado_chassi', 'usado_py', 
        'usado_my', 'usado_cor'
    ]
    for field in fields:
        if field not in st.session_state:
            st.session_state[field] = ''

    # Use a form for better user experience (submits all at once)
    with st.form(key='sales_form'):
        TIPO_VENDA = st.radio('Tipo de Venda:', ["Varejo", "Faixa 0 (Produtor Rural)", "Faixa 1", "Faixa 2", "ABLA", "PCD", "Funcionário", "COMPRA"])

        st.subheader('Cliente:')
        CLIENTE = st.text_input('Nome:')
        CPF = st.text_input('CPF/CNPJ (Somente números):')
        RG = st.text_input('RG:')
        DATA_NASCIMENTO = st.date_input(
            label='Data de Nascimento:',
            min_value=dt.date(1920, 1, 1),
            format=('DD/MM/YYYY')
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
        COMBUSTIVEL = st.radio('Combustível:', ["Álcool / Gasolina", "Gasolina", "Diesel", "GNV", "Elétrico"])
        COR = st.text_input('Cor:')
        PY = st.text_input('Ano de Produção:')
        MY = st.text_input('Ano do Modelo:')
        CHASSI = st.text_input('Chassi:')
        PRECO = st.text_input('Preço (R$):')
        PLACA = st.text_input('Placa: (Preencher se for usado)')
        RENAVAM = st.text_input('RENAVAM:')

        st.subheader('Veículo Usado:')

        uploaded_file = st.file_uploader("Foto CRLV", type=["jpg", "jpeg", "png", "pdf"])

        # Initialize session state for managing upload
        if 'process_file' not in st.session_state:
            st.session_state.process_file = False

        process_button = st.form_submit_button("Process CRLV")
        
        # Check if there's a file and the process button was pressed
        if uploaded_file is not None and process_button:
            st.session_state.process_file = True
        else:
            st.session_state.process_file = False

        if st.session_state.process_file:
            content = process_crlv(uploaded_file)
            try:
                crlv_usado_data = get_crlv_data(content)
                # Update session state based on processed data
                # Only attempt to split if "marca_modelo" is in crlv_usado_data and not None
                if crlv_usado_data.get("marca_modelo"):
                    marca_modelo_split = crlv_usado_data["marca_modelo"].split("/")
                    st.session_state.usado_marca = marca_modelo_split[0].strip() if len(marca_modelo_split) > 0 else ""
                    st.session_state.usado_modelo = marca_modelo_split[1].strip() if len(marca_modelo_split) > 1 else ""
                else:
                    st.session_state.usado_marca = ''
                    st.session_state.usado_modelo = ''
                st.session_state.usado_placa = crlv_usado_data.get('placa', "")
                st.session_state.usado_renavam = crlv_usado_data.get('renavam', "")
                st.session_state.usado_chassi = crlv_usado_data.get('chassi', "")
                st.session_state.usado_py = crlv_usado_data.get('py', "")
                st.session_state.usado_my = crlv_usado_data.get('my', "")
                st.session_state.usado_cor = crlv_usado_data.get('cor', "")
                st.write("Checar informações!")
            except Exception as e:
                st.error(f"Error processing document: {e}")

        USADO_MARCA = st.text_input('Marca Veículo Usado:', value=st.session_state.usado_marca)
        USADO_MODELO = st.text_input('Modelo Veículo Usado:', value=st.session_state.usado_modelo)
        USADO_PY = st.text_input('Ano Produção:', value=st.session_state.usado_py)
        USADO_MY = st.text_input('Ano Modelo:', value=st.session_state.usado_my)
        USADO_PLACA = st.text_input('Placa do Veículo Usado:', value=st.session_state.usado_placa)
        USADO_RENAVAM = st.text_input('RENAVAM do Veículo Usado:', value=st.session_state.usado_renavam)
        USADO_CHASSI = st.text_input('Chassi do Veículo Usado:', value=st.session_state.usado_chassi)
        USADO_COR = st.text_input('Cor do Veículo Usado:', value=st.session_state.usado_cor)
        USADO_VALOR = st.text_input('Valor (R$):')
        USADO_KM = st.text_input('KM do Veículo Usado:')
        USADO_QUITACAO = st.text_input('Quitação:')
        LOJA = st.radio("Loja compradora:", ["Promenac Matriz", "Camvel", "Caninana", "Brava", "Porto Belo", "Penha", "Navegantes"])

        st.subheader('Preencher se for diferente Proprietário')
        PROPRIETARIO_NOME = st.text_input('Nome do Proprietário:')
        PROPRIETARIO_CPF = st.text_input('CPF/CNPJ do Proprietário:')
        PROPRIETARIO_RG = st.text_input('RG do Proprietário:')
        PROPRIETARIO_ENDERECO = st.text_input('Endereço do Proprietário:')
        PROPRIETARIO_CIDADE = st.text_input('Cidade do Proprietário:')
        PROPRIETARIO_ESTADO = st.text_input('Estado do Proprietário:')

        st.subheader('Forma de Pagamento:')
        NF = st.text_input('Valor Nota Fiscal (R$):')
        FINANCIAMENTO = st.text_input('Valor Financiado (R$):')
        BANCO = st.text_input('Banco:')
        N_PARCELAS = st.text_input('Número de Parcelas:')
        VALOR_PARCELA = st.text_input('Valor Parcela (R$)')
        NEGOCIACAO = st.text_area('Forma de Pagamento: (Máximo 6 linhas)')
        OBSERVACAO = st.text_input('Observações (Cortesias):')

        st.subheader('Serviços:')
        free = 'Loja'
        cust = 'Cliente'
        EMPLACAMENTO_PGTO = st.radio('Emplacamento/Transferência', [cust, free], horizontal=True)
        EMPLACAMENTO = st.text_input('Observação Emplacamento/Transferência:')
        IPVA_PGTO = st.radio('IPVA', [cust, free], horizontal=True)
        IPVA = st.text_input('Observação IPVA:')
        ESCOLHA_PLACA_PGTO = st.radio('Escolha de Placa', ['Não', cust, free], horizontal=True)
        ESCOLHA_PLACA = st.text_input('Observação Escolha de Placa:')
        OUTROS = st.text_input('Outros:')
        OUTROS_PGTO = st.radio('Outros', ['Não', cust, free], horizontal=True)

        st.subheader('Retirada:')
        AUTORIZACAO = st.checkbox('Outra pessoa irá retirar o veículo')
        AUTORIZACAO_AUTORIZADO = st.text_input('Nome da pessoa:')

        st.subheader('Assinatura:')
        LOCAL = st.text_input('Local:')
        DATA_ASSINATURA = st.date_input(label='Data:', format='DD/MM/YYYY')

        # Form submit button
        submit_button = st.form_submit_button(label='Submit')

    # Process the form data when the button is pressed
    if submit_button:

        if not CPF.isdigit():
            st.error("CPF/CNPJ inválido. Favor digitar apenas números.")

        else:
            form_data = {
                'TIPO_VENDA': TIPO_VENDA,
                'CLIENTE': CLIENTE,
                'CPF': CPF,
                'RG': RG,
                'DATA_NASCIMENTO': DATA_NASCIMENTO.strftime('%d/%m/%Y'),
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

                'USADO_VEICULO': USADO_MARCA + " / " + USADO_MODELO,
                'USADO_VALOR': USADO_VALOR,
                'USADO_PLACA': USADO_PLACA,
                'USADO_RENAVAM': USADO_RENAVAM,
                'USADO_CHASSI': USADO_CHASSI,
                'USADO_COR': USADO_COR,
                'USADO_PY_MY': USADO_PY + "/" + USADO_MY,
                'USADO_KM': USADO_KM,
                'USADO_QUITACAO': USADO_QUITACAO,
                'LOJA': LOJA,

                'PROPRIETARIO_NOME': PROPRIETARIO_NOME,
                'PROPRIETARIO_CPF': PROPRIETARIO_CPF,
                'PROPRIETARIO_RG': PROPRIETARIO_RG,
                'PROPRIETARIO_ENDERECO': PROPRIETARIO_ENDERECO,
                'PROPRIETARIO_CIDADE': PROPRIETARIO_CIDADE,
                'PROPRIETARIO_ESTADO': PROPRIETARIO_ESTADO,

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
                'EMPLACAMENTO': EMPLACAMENTO,
                'IPVA_PGTO': IPVA_PGTO,
                'IPVA': IPVA,
                'ESCOLHA_PLACA_PGTO': ESCOLHA_PLACA_PGTO,
                'ESCOLHA_PLACA': ESCOLHA_PLACA,
                'OUTROS': OUTROS,
                'OUTROS_PGTO': OUTROS_PGTO,

                'LOCAL': LOCAL,
                'DIA': str(DATA_ASSINATURA.day).zfill(2),
                'MES': str(DATA_ASSINATURA.month).zfill(2),
                'ANO': str(DATA_ASSINATURA.year)
            }

            form_data = process_form_data(form_data)

            notion_client = initialize_notion_client()
            add_form_data_to_notion(notion_client, form_data)

            st.write("Form Submitted.")

            pdf_paths = []

            # Always fill the primary PDF template
            pdf_paths.append(create_pdf_and_return_path("Templates/Ficha de vendas - V6.pdf", form_data, "FV", font_size=9))

            # Convert months to written
            months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Março', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
            month_index = int(form_data['MES'])
            form_data['MES'] = months[month_index - 1]

            # Fill Procuração de Comprador based on CPF length
            if form_data.get("PLACA", "") != "" or form_data.get("USADO_VEICULO", "") != "":
                if form_data.get("PESSOA_FISICA", "") == "S":
                    pdf_paths.append(create_pdf_and_return_path("Templates/PROCURAÇÃO DE COMPRADOR PF.pdf", form_data, "Proc"))
                elif form_data.get("PESSOA_FISICA", "") == "N":
                    pdf_paths.append(create_pdf_and_return_path("Templates/PROCURAÇÃO DE COMPRADOR PJ.pdf", form_data, "Proc"))

            # Change customer values if other proprietor
            if form_data.get("PROPRIETARIO_NOME", "") != "":
                cust = form_data.get("CLIENTE", "unk")
                form_data = process_other_proprietor(form_data)
                form_data = process_cpf(form_data)

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
                        file_name=f"DOCS_{cust}.zip",
                        mime="application/zip"
                    )

if __name__ == "__main__":
    main()