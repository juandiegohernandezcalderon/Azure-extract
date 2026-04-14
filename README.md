# 🚀 Azure DevOps Data Extractor

Este script de Python permite extraer información de **Work Items** desde Azure DevOps de forma automatizada. Utiliza un archivo de Excel como base para saber qué campos debe consultar y genera un reporte en formato **CSV**.

## 🛠️ Funcionalidades

* **Lectura Dinámica:** Obtiene los nombres de los campos directamente desde un archivo Excel (`.xlsx`).
* **Conexión con API REST:** Utiliza la API de Azure DevOps para realizar consultas WIQL.
* **Filtro Personalizado:** Extrae los últimos 200 Work Items modificados (ajustable).
* **Exportación Limpia:** Genera un archivo `workitems_export.csv` listo para análisis en Excel o Power BI.

## 📋 Requisitos Previos

Antes de ejecutar el script, asegúrate de tener instalado Python y las siguientes librerías:

```bash
pip install requests pandas openpyxl
