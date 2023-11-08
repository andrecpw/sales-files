from PyPDF2 import PdfReader, PdfWriter

def fill_pdf(input_pdf_path, output_pdf_path, form_data):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Access the form fields in the PDF and fill them in with the data from form_data
    for page in reader.pages:
        try:
            writer.add_page(page)
            fields = page.get_fields()
            for field_name, field_value in form_data.items():
                if field_name in fields:
                    fields[field_name].value = field_value
        except Exception as e:
            print(f"An error occurred: {e}")

    # Write out the filled PDF to a new file
    with open(output_pdf_path, "wb") as output_stream:
        writer.write(output_stream)

# Example usage
if __name__ == "__main__":
    template_pdf_path = "Templates/NOVA Ficha de Vendas V4.pdf"  # Replace with your PDF template path
    filled_pdf_path = f"Output/FV_{form_data[name].replace(" ", "_")}.pdf"      # Replace with the desired output PDF path
    form_data

    fill_pdf(template_pdf_path, filled_pdf_path, form_data)
