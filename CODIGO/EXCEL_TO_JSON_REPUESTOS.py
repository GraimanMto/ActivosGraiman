import pandas as pd
import os
import json

# Ruta de tu archivo Excel de repuestos
excel_path = r"C:\Users\bryam\Desktop\PRACTICAS GRAIMA\MOTORES\QR\BETA\Repuestos.xlsx"  # <-- cambia esto a tu ruta real

# Ruta de la carpeta donde se guardarán los archivos JSON
output_dir = r"C:\Users\bryam\Desktop\PRACTICAS GRAIMA\MOTORES\QR\BETA\CODIGO GENERAL\github_pages\json_activos"  # <-- carpeta donde tienes tu localhost
os.makedirs(output_dir, exist_ok=True)

# Leer el Excel
df = pd.read_excel(excel_path)

# Extraer el prefijo del activo (ej. "H1-HO01" de "H1-HO01-VE01")
df["Prefijo"] = df["Nro Activo"].str.extract(r"^([A-Z0-9]+-[A-Z0-9]+)")

# Crear un JSON por cada activo
for prefijo, grupo in df.groupby("Prefijo"):
    repuestos = []
    for _, row in grupo.iterrows():
        repuestos.append({
            "Articulo": row["Codigo Producto Pieza"],
            "Descripcion": row["Nombre"],
            "Cantidad": int(row["Cantidad Pieza"]),
            "UM": row["Uom Pieza"]
        })
    
    # Guardar archivo JSON
    json_data = {"repuestos": repuestos}
    json_path = os.path.join(output_dir, f"{prefijo}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

print("✅ Archivos JSON generados correctamente en:", output_dir)
