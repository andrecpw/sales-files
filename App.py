import streamlit as st
import datetime as dt

# Function to process the form data (this is where you would add your PDF filling logic)
def process_form_data(form_data):
    # You can process and save the data, or generate a PDF using a library like PyPDF2 or reportlab
    st.write("Form Submitted. Here's the data:")
    st.json(form_data)  # For demonstration, just display the data as JSON in the app

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
        payment_form = st.text_area('Forma de Pagamento:', key='payment_form')

        st.subheader('Observações:')
        observations = st.text_input('Observações:')
        authorization = st.checkbox('Autorizo a retirar o veículo acima descrito')

        st.subheader('Serviços:')
        free = 'Loja'
        cust = 'Cliente'
        emplacamento = st.radio('Emplacamento/Transferência', [free, cust], horizontal=True)
        ipva = st.radio('IPVA', [free, cust], horizontal=True)
        plate_choice = st.radio('Escolha de Placa', [free, cust], horizontal=True)
        plate_choice_text = st.text_input('Observação Escolha de Placa:')
        other_text = st.text_input('Outros:')
        other = st.radio('Outros', [free, cust], horizontal=True)

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