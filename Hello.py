import streamlit as st
from datetime import date

# Function to process the form data (this is where you would add your PDF filling logic)
def process_form_data(form_data):
    # You can process and save the data, or generate a PDF using a library like PyPDF2 or reportlab
    st.write("Form Submitted. Here's the data:")
    st.json(form_data)  # For demonstration, just display the data as JSON in the app

def main():
    # Set page config
    st.set_page_config(page_title="Ficha de Vendas", page_icon="📝")

    st.title('Ficha de Vendas')

    # Use a form for better user experience (submits all at once)
    with st.form(key='sales_form'):
        st.subheader('Cliente:')
        name = st.text_input('Nome:')
        cpf = st.text_input('CPF:')
        rg = st.text_input('RG:')
        birth_date = st.date_input(
            label='Data de Nascimento:',
            min_value=date(1920, 1, 1),
            format="DD/MM/YYYY"
        )
        phone = st.text_input('Telefone:')
        mobile = st.text_input('Celular:')
        street = st.text_input('Rua:')
        street_no = st.text_input('No:')
        district = st.text_input('Bairro:')
        city = st.text_input('Cidade:')
        cep = st.text_input('CEP:')
        email = st.text_input('Email:')

        st.subheader('Negociação:')
        vehicle = st.text_input('Veículo:')
        model = st.text_input('Modelo:')
        color = st.text_input('Cor:')
        year_model = st.text_input('Ano/Modelo:')
        chassis = st.text_input('Chassi:')
        price = st.text_input('Preço:')
        plate = st.text_input('Placa:')

        st.subheader('Veículo Usado:')
        used_plate = st.text_input('Placa do Veículo Usado:', key='used_plate')
        renavam = st.text_input('RENAVAM do Veículo Usado:', key='renavam')
        chassis_used = st.text_input('Chassi do Veículo Usado:', key='chassis_used')
        km = st.text_input('KM do Veículo Usado:', key='km')
        payment_form = st.text_area('Forma de Pagamento:', key='payment_form')

        st.subheader('Observações:')
        observations = st.text_area('Observações:')
        authorization = st.checkbox('Autorizo a retirar o veículo acima descrito')

        st.subheader('Serviços:')
        emplacamento = st.checkbox('Emplacamento/Transferência')
        ipva = st.checkbox('IPVA')
        plate_choice = st.checkbox('Escolha de Placa')

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
            'color': color,
            'year_model': year_model,
            'chassis': chassis,
            'price': price,
            'plate': plate,
            'used_plate': used_plate,
            'renavam': renavam,
            'chassis_used': chassis_used,
            'km': km,
            'payment_form': payment_form,
            'observations': observations,
            'authorization': authorization,
            'emplacamento': emplacamento,
            'ipva': ipva,
            'plate_choice': plate_choice
        }
        process_form_data(form_data)

if __name__ == "__main__":
    main()