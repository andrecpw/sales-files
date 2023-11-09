import pdfrw

def fill_pdf(input_pdf_path, output_pdf_path, form_data):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0]['/Annots']

    for annotation in annotations:
        if annotation['/Subtype'] == '/Widget':
            if annotation['/T']:
                key = annotation['/T'][1:-1]  # Remove parentheses
                if key in form_data:
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(form_data[key]))
                    )

    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

# Example usage
if __name__ == "__main__":
    template_pdf_path = "Templates/NOVA Ficha de Vendas V4.pdf"
    form_data = {
        "name":"ANDRE CESARIO PEREIRA WERNER",
        "cpf":"07521372980",
        "rg":"5415555",
        "birth_date":"2023-11-08",
        "phone":"4799278604",
        "mobile":"47999278604",
        "street":"Rua 1001",
        "street_no":"348",
        "district":"Centro",
        "city":"Florianópolis",
        "cep":"88015-510",
        "email":"andre_cpw@hotmail.com",
        "vehicle":"Polo",
        "model":"Highline",
        "optionals":"PF2",
        "color":"Branco",
        "year_model":"2019/2020",
        "chassis":"9BW3489BR23482",
        "price":"49.990,00",
        "plate":"QIE9420",
        "used_vehicle":"Up! HL",
        "used_value":"29.990,00",
        "used_plate":"MIE2938",
        "renavam":"32849234923",
        "used_chassis":"9NQ3489BRT90R",
        "used_color":"Azul",
        "used_py":"2017",
        "used_my":"2018",
        "km":"39000",
        "debt":"0",
        "nf":"49.990,00",
        "financing":"30,000.00",
        "bank":"Santander",
        "n_payments":"48",
        "installments":"499,00",
        "payment_form":"Dinheiro 20.000,00\nAbracadabra 10.000,00\n2390423234230",
        "observations":"Emplacamento cortesia",
        "authorization":False,
        "auth_retriever":"",
        "emplacamento":"Loja",
        "ipva":"Cliente",
        "ipva_free":"True",
        "plate_choice_cust":"True",
        "plate_choice_text":"QIE9259",
        "other_text":"",
        "other":"Cliente"
    }
    filled_pdf_path = f"Output/FV_{form_data['name']}.pdf"

    fill_pdf(template_pdf_path, filled_pdf_path, form_data)
