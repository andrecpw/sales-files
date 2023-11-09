import streamlit as st
import datetime as dt
from Scripts.pdf_generator import fill_pdf, flatten_pdf

# Function to process the form data (this is where you would add your PDF filling logic)
def process_form_data(form_data):
    # You can process and save the data, or generate a PDF using a library like PyPDF2 or reportlab
    if form_data["emplacamento"] == "Loja":
        form_data["emplacamento_free"] = "True"
    elif form_data["emplacamento"] == "Cliente":
        form_data["emplacamento_cust"] = "True"

    if form_data["ipva"] == "Loja":
        form_data["ipva_free"] = "True"
    elif form_data["ipva"] == "Cliente":
        form_data["ipva_cust"] = "True"

    if form_data["plate_choice"] == "Loja":
        form_data["plate_choice_free"] = "True"
    elif form_data["plate_choice"] == "Cliente":
        form_data["plate_choice_cust"] = "True"

    if form_data["other"] == "Loja":
        form_data["other_free"] = "True"
    elif form_data["other"] == "Cliente":
        form_data["other_cust"] = "True"

    st.write("Form Submitted.")
    
    return form_data

# Set page config
st.set_page_config(page_title="Ficha de Vendas", page_icon="📝")

def main():

    st.title('Ficha de Vendas')

    # Use a form for better user experience (submits all at once)
    with st.form(key='sales_form'):
        st.subheader('Cliente:')
        name = st.text_input('Nome:')
        cpf = st.text_input('CPF:')
        rg = st.text_input('RG:')
        birth_date = st.date_input(
            label='Data de Nascimento:',
            min_value=dt.date(1920, 1, 1),
            format=("DD/MM/YYYY")
        )
        mobile = st.text_input('Celular:')
        phone = st.text_input('Telefone:')
        street = st.text_input('Rua:')
        street_no = st.text_input('Número:')
        district = st.text_input('Bairro:')
        city = st.text_input('Cidade:')
        cep = st.text_input('CEP:')
        email = st.text_input('Email:')

        st.subheader('Negociação:')
        vehicle = st.text_input('Veículo:')
        model = st.text_input('Modelo:')
        optionals = st.text_input('Opcionais:')
        color = st.text_input('Cor:')
        year_model = st.text_input('Ano/Modelo:')
        chassis = st.text_input('Chassi:')
        price = st.text_input('Preço:')
        plate = st.text_input('Placa:')

        st.subheader('Veículo Usado:')
        used_vehicle = st.text_input('Veículo Usado:')
        used_value = st.text_input('Valor:')
        used_plate = st.text_input('Placa do Veículo Usado:', key='used_plate')
        renavam = st.text_input('RENAVAM do Veículo Usado:', key='renavam')
        used_chassis = st.text_input('Chassi do Veículo Usado:', key='used_chassis')
        used_color = st.text_input('Cor:', key='used_color')
        used_py = st.text_input('Ano Produção:')
        used_my = st.text_input('Ano Modelo:')
        km = st.text_input('KM do Veículo Usado:', key='km')
        debt = st.text_input('Quitação:')

        st.subheader('Forma de Pagamento:')
        nf = st.text_input('Valor Nota Fiscal:')
        financing = st.text_input('Valor Financiado:')
        bank = st.text_input('Banco:')
        n_payments = st.text_input('Número de Parcelas:')
        installments = st.text_input('Valor Parcela')
        #TODO figure out the text area size
        payment_form = st.text_area('Forma de Pagamento:', key='payment_form')

        st.subheader('Observações:')
        observations = st.text_input('Observações:')
        authorization = st.checkbox('Outra pessoa irá retirar o veículo')
        auth_retriever = st.text_input('Nome da pessoa:')

        st.subheader('Serviços:')
        free = 'Loja'
        cust = 'Cliente'
        emplacamento = st.radio('Emplacamento/Transferência', [cust, free], horizontal=True)
        ipva = st.radio('IPVA', [cust, free], horizontal=True)
        plate_choice = st.radio('Escolha de Placa', ['Não', cust, free], horizontal=True)
        plate_choice_text = st.text_input('Observação Escolha de Placa:')
        other_text = st.text_input('Outros:')
        other = st.radio('Outros', ['Não', cust, free], horizontal=True)

        # Form submit button
        submit_button = st.form_submit_button(label='Submit')

    # Process the form data when the button is pressed
    if submit_button:
        form_data = {
            'name': name,
            'cpf': cpf,
            'rg': rg,
            'birth_date': str(birth_date),
            'phone': phone,
            'mobile': mobile,
            'street': street,
            'street_no': street_no,
            'district': district,
            'city': city,
            'cep': cep,
            'email': email,
            'vehicle': vehicle,
            'model': model,
            'optionals': optionals,
            'color': color,
            'year_model': year_model,
            'chassis': chassis,
            'price': price,
            'plate': plate,
            'used_vehicle': used_vehicle,
            'used_value': used_value,
            'used_plate': used_plate,
            'renavam': renavam,
            'used_chassis': used_chassis,
            'used_color': used_color,
            'used_py': used_py,
            'used_my': used_my,
            'km': km,
            'debt': debt,
            'nf': nf,
            'financing': financing,
            'bank': bank,
            'n_payments': n_payments,
            'installments': installments,
            'payment_form': payment_form,
            'observations': observations,
            'authorization': authorization,
            'auth_retriever': auth_retriever,
            'emplacamento': emplacamento,
            'ipva': ipva,
            'plate_choice': plate_choice,
            'plate_choice_text': plate_choice_text,
            'other_text': other_text,
            'other': other
        }
        form_data = process_form_data(form_data)

        template_pdf_path = "Templates/NOVA Ficha de Vendas V4.pdf"
        filled_pdf_path = f"Output/FV_{form_data['name']}_formatavel.pdf"
        fill_pdf(template_pdf_path, filled_pdf_path, form_data)
        flatten_pdf(f"Output/FV_{form_data['name']}_formatavel.pdf", f"Output/FV_{form_data['name']}.pdf")

        # Create a link to download the PDF
        with open(filled_pdf_path, "rb") as file:
            st.download_button(
                label="Download Ficha de Vendas",
                data=file,
                file_name=f"FV_{form_data['name']}_formatavel.pdf",
                mime="application/octet-stream"
            )
        with open(filled_pdf_path, "rb") as file:
            st.download_button(
                label="Download Ficha de Vendas",
                data=file,
                file_name=f"FV_{form_data['name']}.pdf",
                mime="application/octet-stream"
            )


if __name__ == "__main__":
    main()