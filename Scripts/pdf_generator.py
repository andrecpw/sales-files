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