from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject

def fill_pdf(input_pdf_path, output_pdf_path, form_data):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        annotations = page.get("/Annots")
        if annotations is not None:
            for annotation in annotations:
                if isinstance(annotation, IndirectObject):
                    annotation = annotation.get_object()

                if annotation.get("/Subtype") == "/Widget" and annotation.get("/T"):
                    field_name = annotation["/T"][1:-1]  # Remove parentheses
                    if field_name in form_data and form_data[field_name] is not None:
                        annotation.update({
                            NameObject("/V"): form_data[field_name]
                        })

        writer.add_page(page)

    with open(output_pdf_path, 'wb') as output_stream:
        writer.write(output_stream)
