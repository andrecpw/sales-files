from PyPDF2 import PdfReader, PdfWriter

def fill_pdf(input_pdf_path, output_pdf_path, form_data):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Iterate through each page in the PDF
    for page in reader.pages:
        # Get the fields in the current page
        fields = page.get('/Annots')

        if fields is not None:
            for field in fields:
                # Resolve indirect object references
                field = field.get_object()
                
                # Check if it is a form field (widget annotation)
                if field.get('/Subtype') == '/Widget' and field.get('/T'):
                    field_name = field['/T'].strip('()')
                    
                    # Update the field value if the field name is in form_data
                    if field_name in form_data and form_data[field_name] is not None:
                        field.update({
                            '/V': form_data[field_name]
                        })
            
            # Update the page with modified fields
            writer.add_page(page)

    # Write the output PDF file
    with open(output_pdf_path, 'wb') as output_stream:
        writer.write(output_stream)
