from PyPDF2 import PdfReader, PdfWriter, PdfName

def fill_pdf(input_pdf_path, output_pdf_path, form_data):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Iterate through each page in the PDF
    for page in reader.pages:
        # Get the annotations (fields) in the current page
        annotations = page.get("/Annots")

        # Check if annotations exist
        if annotations:
            # Resolve each annotation if it is an indirect object
            for annotation in annotations:
                if isinstance(annotation, IndirectObject):
                    annotation = annotation.get_object()
                
                # Check if it is a form field (widget annotation)
                if annotation.get("/Subtype") == "/Widget" and annotation.get("/T"):
                    field_name = annotation["/T"].strip("()")

                    # Update the field value if the field name is in form_data
                    if field_name in form_data and form_data[field_name] is not None:
                        annotation.update({
                            PdfName("/V"): form_data[field_name]
                        })

        # Add the updated page to the writer
        writer.add_page(page)

    # Write the output PDF file
    with open(output_pdf_path, "wb") as output_stream:
        writer.write(output_stream)