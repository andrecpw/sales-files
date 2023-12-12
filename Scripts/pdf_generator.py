import pdfrw
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject

def fill_pdf(input_pdf_path, output_pdf_path, form_data, font_size=None):
    template_pdf = PdfReader(input_pdf_path)

    for page in template_pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation.get("/Subtype") == "/Widget" and annotation.get("/T"):
                    key = annotation["/T"][1:-1]  # Remove parentheses
                    if key in form_data:
                        annotation.update(
                            pdfrw.PdfDict(V="{}".format(form_data[key]))
                        )
                        annotation.update(PdfDict(AP=""))

                        # Set font size if specified
                        if font_size:
                            annotation.update(PdfDict(DA=f"/Arial {font_size} Tf"))

    # Flag the form to update appearances
    if "/AcroForm" in template_pdf.Root:
        template_pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))

    PdfWriter().write(output_pdf_path, template_pdf)


# Function to create a PDF and return its path with a custom name
def create_pdf_and_return_path(template_path, form_data, prefix, font_size=None):
    # Create a temporary file with a custom name
    cust = form_data.get("CLIENTE", "unk")
    fd, path = tempfile.mkstemp(suffix=".pdf", prefix=f"{prefix}_{cust}_")
    os.close(fd)  # Close the file descriptor

    # Fill the PDF with data
    fill_pdf(template_path, path, form_data, font_size)
    return path