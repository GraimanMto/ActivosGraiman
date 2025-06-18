import pandas as pd
import os
import json

# Ruta del archivo Excel de repuestos
excel_path = r"C:\Users\bryam\Desktop\PRACTICAS GRAIMA\Activos_directorio\Repuestos.xlsx"

# Carpeta de salida para los archivos JSON
output_dir = r"C:\Users\bryam\Desktop\PRACTICAS GRAIMA\Activos_directorio\json_activos"
os.makedirs(output_dir, exist_ok=True)

# Leer el archivo Excel
df = pd.read_excel(excel_path)

# Crear un JSON por cada activo según 'Nro Activo'
for nro_activo, grupo in df.groupby("Nro Activo"):
    repuestos = []
    for _, row in grupo.iterrows():
        repuestos.append({
            "Articulo": row["Codigo Producto Pieza"],
            "Descripcion": row["Nombre"],
            "Cantidad": int(row["Cantidad Pieza"]),
            "UM": row["Uom Pieza"]
        })

    json_data = {"repuestos": repuestos}
    json_filename = f"{nro_activo}.json"
    json_path = os.path.join(output_dir, json_filename)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

print("✅ Archivos JSON generados correctamente en:", output_dir)
