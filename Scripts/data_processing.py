
# Function to process the form data (this is where you would add your PDF filling logic)
def process_form_data(form_data):
    # You can process and save the data, or generate a PDF using a library like PyPDF2 or reportlab
    if form_data["EMPLACAMENTO_PGTO"] == "Loja":
        form_data["EMPLACAMENTO_LOJA"] = "X"
    elif form_data["EMPLACAMENTO_PGTO"] == "Cliente":
        form_data["EMPLACAMENTO_CLIENTE"] = "X"

    if form_data["IPVA_PGTO"] == "Loja":
        form_data["IPVA_LOJA"] = "X"
    elif form_data["IPVA_PGTO"] == "Cliente":
        form_data["IPVA_CLIENTE"] = "X"

    if form_data["ESCOLHA_PLACA_PGTO"] == "Loja":
        form_data["ESCOLHA_PLACA_LOJA"] = "X"
    elif form_data["ESCOLHA_PLACA_PGTO"] == "Cliente":
        form_data["ESCOLHA_PLACA_CLIENTE"] = "X"

    if form_data["OUTROS_PGTO"] == "Loja":
        form_data["OUTROS_LOJA"] = "X"
    elif form_data["OUTROS_PGTO"] == "Cliente":
        form_data["OUTROS_CLIENTE"] = "X"

    if form_data.get("AUTORIZACAO_AUTORIZADO", "") != "":
        form_data["AUTORIZACAO_CLIENTE"] = form_data["CLIENTE"]

    # Process the NEGOCIACAO field
    negociacao_parts = form_data.get("NEGOCIACAO", "").split('\n')
    for i in range(1, 7):
        form_data[f"NEGOCIACAO_{i}"] = negociacao_parts[i - 1] if i <= len(negociacao_parts) else ""

    # Process LOJA if Used_car
    if form_data.get("PLACA", "") != "" or form_data.get("USADO_VEICULO", "") != "":
        if form_data.get("LOJA") == "Promenac Matriz":
            form_data["LOJA"] = "REVENDEDORES PROMENAC LTDA"
            form_data["LOJA_CNPJ"] = "84.290.907/0001-22"
            form_data["LOJA_ENDERECO"] = "RUA EXPEDICIONÁRIO ALEIXO AMABA, 60 - BARRA DO RIO"
            form_data["LOJA_CIDADE"] = "ITAJAÍ / SC"
        elif form_data.get("LOJA") == "Camvel":
            form_data["LOJA"] = "CAMBORIÚ COMÉRCIO DE VEÍCULOS LTDA"
            form_data["LOJA_CNPJ"] = "83.115.493/0001-32"
            form_data["LOJA_ENDERECO"] = "AV. MARGINAL LESTE , N° 3500 - DOS ESTADOS"
            form_data["LOJA_CIDADE"] = "BALNEÁRIO CAMBORIÚ / SC"
        elif form_data.get("LOJA") == "Caninana":
            form_data["LOJA"] = "REVENDEDORES PROMENAC LTDA"
            form_data["LOJA_CNPJ"] = "84.290.907/0003-94"
            form_data["LOJA_ENDERECO"] = "AV. IRINEU BORNHAUSEN, N° 301 - SÃO JOÃO"
            form_data["LOJA_CIDADE"] = "ITAJAÍ / SC"
        elif form_data.get("LOJA") == "Brava":
            form_data["LOJA"] = "REVENDEDORES PROMENAC LTDA"
            form_data["LOJA_CNPJ"] = "84.290.907/0002-03"
            form_data["LOJA_ENDERECO"] = "RODOVIA OSVALDO REIS, N° 2455 - FAZENDA"
            form_data["LOJA_CIDADE"] = "ITAJAÍ / SC"
        elif form_data.get("LOJA") == "Porto Belo":
            form_data["LOJA"] = "CAMBORIÚ COMÉRCIO DE VEÍCULOS LTDA"
            form_data["LOJA_CNPJ"] = "83.115.493/0003-02"
            form_data["LOJA_ENDERECO"] = "AV. GOVERNADOR CELSO RAMOS, N° 1393 - PEREQUÊ"
            form_data["LOJA_CIDADE"] = "PORTO BELO / SC"
        elif form_data.get("LOJA") == "Penha":
            form_data["LOJA"] = "REVENDEDORES PROMENAC LTDA"
            form_data["LOJA_CNPJ"] = "84.290.907/0006-37"
            form_data["LOJA_ENDERECO"] = "AV. PREFEITO EUGENIO KRAUSE, N° 283 - CENTRO"
            form_data["LOJA_CIDADE"] = "PENHA / SC"
        elif form_data["LOJA"] == "Navegantes":
            form_data["LOJA"] = "REVENDEDORES PROMENAC LTDA"
            form_data["LOJA_CNPJ"] = "84.290.907/0007-18"
            form_data["LOJA_ENDERECO"] = "AV. NEREU LIBERATO NUNES, N° 757 - SÃO DOMINGOS"
            form_data["LOJA_CIDADE"] = "NAVEGANTES / SC"


    # Convert all string values to uppercase
    form_data = {key: (value.upper() if value is not None else None) 
             for key, value in form_data.items() if isinstance(value, str)}

    # Process CPF and CNPJ
    number = form_data.get("CPF", None)
    if number:
        if len(number) == 11:  # CPF
            form_data["PESSOA_FISICA"] = "S"
            form_data["CPF"] = f"{number[:3]}.{number[3:6]}.{number[6:9]}-{number[9:]}"
        elif len(number) == 14:  # CNPJ
            form_data["PESSOA_FISICA"] = "N"
            form_data["CPF"] = f"{number[:2]}.{number[2:5]}.{number[5:8]}/{number[8:12]}-{number[12:]}"
    
    return form_data