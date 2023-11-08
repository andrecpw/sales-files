from PyPDF2 import PdfReader, PdfWriter

rel_path = 'Templates\NOVA Ficha de Vendas V4.pdf'
reader = PdfReader(rel_path)

print(reader.get_form_text_fields())