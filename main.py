import requests
import pandas as pd
import os
import json
from requests.auth import _basic_auth_str

# ==========================
# CONFIGURACIÓN DEL USUARIO
# ==========================

# URL base y proyecto (a partir de tu enlace)
organization = "https://dev.azure.com/diego-dev"
project = "Azure-Data-Automation"

# Ruta al archivo Excel con los campos
excel_file = "modelo_datos_azure.xlsx"

# ==========================
# TOKEN PERSONAL (PAT)
# ==========================
# Puedes definirlo como variable de entorno o ingresarlo manualmente

personal_access_token = os.getenv("AZURE_DEVOPS_PAT")

if not personal_access_token:
    personal_access_token = input("👉 Ingresa tu Personal Access Token (PAT): ").strip()

# ==========================
# 1️⃣ Leer el Excel y extraer todos los nombres de campo
# ==========================

df = pd.read_excel(excel_file, sheet_name="Tablas")

# Buscar todas las columnas que contengan "Field Name" o "Field Reference Name"
field_cols = [col for col in df.columns if "Field" in str(col)]
fields = pd.unique(df[field_cols].values.ravel())
fields = [f for f in fields if isinstance(f, str) and f.strip() != ""]
print(f"✅ Campos encontrados ({len(fields)}):")
print(fields)

# ==========================
# 2️⃣ Autenticación con Azure DevOps
# ==========================

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {_basic_auth_str("", personal_access_token)}'
}

# ==========================
# 3️⃣ Consultar Work Items (últimos 200)
# ==========================

wiql_query = {
    "query": "SELECT [System.Id] FROM WorkItems ORDER BY [System.ChangedDate] DESC"
}

url_wiql = f"{organization}/{project}/_apis/wit/wiql?api-version=7.1"
response = requests.post(url_wiql, headers=headers, json=wiql_query)
response.raise_for_status()

work_items = response.json().get("workItems", [])
work_item_ids = [str(item["id"]) for item in work_items]

if not work_item_ids:
    print("⚠️ No se encontraron Work Items.")
    exit()

# ==========================
# 4️⃣ Obtener detalles de los Work Items
# ==========================

ids_str = ",".join(work_item_ids[:200])  # puedes aumentar el límite
fields_str = ",".join(fields)

url_items = f"{organization}/_apis/wit/workitems?ids={ids_str}&fields={fields_str}&api-version=7.1"

resp_details = requests.get(url_items, headers=headers)
resp_details.raise_for_status()
data = resp_details.json()

# ==========================
# 5️⃣ Convertir a DataFrame y exportar CSV
# ==========================

rows = []
for item in data.get("value", []):
    row = {"id": item["id"]}
    for f in fields:
        row[f] = item["fields"].get(f, None)
    rows.append(row)

df_out = pd.DataFrame(rows)
df_out.to_csv("workitems_export.csv", index=False, encoding="utf-8-sig")

print("✅ Exportación completada: workitems_export.csv")
