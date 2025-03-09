import pandas as pd
from base_no_data import load_json, process_json_data, create_dataframe

# Caminho do arquivo JSON
input_file = "path_to.json"
output_file = "nome_do_arquivo.xlsx"

# Carrega os dados
data = load_json(input_file)

# Processa os dados
processed_data = process_json_data(data)
df = create_dataframe(processed_data)

# Salva os dados no Excel
df.to_excel(output_file, index=False)
print(f"Processamento concluído e planilha gerada: {output_file}")
