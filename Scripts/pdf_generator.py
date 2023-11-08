from PyPDF2 import PdfReader, PdfWriter, PdfName

def fill_pdf(input_pdf_path, output_pdf_path, form_data):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Loop through each page in the input PDF
    for page in reader.pages:
        # Retrieve the annotations from the page
        annotations = page.get("/Annots")
        if annotations is None:
            continue

        # Need to resolve each annotation if it is an indirect object
        for annotation in annotations:
            if isinstance(annotation, IndirectObject):
                annotation = annotation.get_object()

            # Check if it is a widget (form field) annotation
            if annotation.get("/Subtype") == "/Widget":
                field_name = annotation.get("/T")
                field_value = form_data.get(field_name)

                # If the field name is in the form data, update the value
                if field_name in form_data and field_value is not None:
                    # Create a new dictionary with updated field value
                    field_dictionary = annotation.get("/AA")
                    if field_dictionary:
                        field_dictionary.update({
                            PdfName("/V"): PdfString(field_value)
                        })

        # Add the updated page to the writer
        writer.add_page(page)

    # Write out the filled PDF to a new file
    with open(output_pdf_path, "wb") as output_stream:
        writer.write(output_stream)

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
        "plate_choice":"Cliente",
        "plate_choice_text":"QIE9259",
        "other_text":"",
        "other":"Cliente"
    }
    filled_pdf_path = f"Output/FV_{form_data['name']}.pdf"

    fill_pdf(template_pdf_path, filled_pdf_path, form_data)
