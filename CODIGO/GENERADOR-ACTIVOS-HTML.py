import pandas as pd
import os
import json
from jinja2 import Environment, FileSystemLoader

# Configuraciones iniciales
output_dir = "github_pages"
padres_dir = os.path.join(output_dir, "padres")
activos_dir = os.path.join(output_dir, "activos")
# images_dir = os.path.join(output_dir, "images")
templates_dir = "templates"
# json_activos_dir = os.path.join(output_dir, "json_activos")
js_dir = os.path.join(output_dir, "js")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(padres_dir, exist_ok=True)
os.makedirs(activos_dir, exist_ok=True)
# os.makedirs(images_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)
# os.makedirs(json_activos_dir, exist_ok=True)
os.makedirs(js_dir, exist_ok=True)

# Leer archivos
csv_df = pd.read_csv("KPI_TECNICO.csv", sep=";", encoding="utf-8")
excel_df = pd.read_excel("DATOS-MOTORES-PLANTA.xlsx")

# Correcciones de nombres
corrections = {
    "Anio Fabricacion": "Año de Fabricación",
    "Año Fabricacion": "Año de Fabricación",
    "Ubicacion": "Ubicación",
    "Descripcion": "Descripción",
    "Pais Origen": "País de Origen",
    "Alimentacion Electrica": "Alimentación Eléctrica",
    "Consumo Energia": "Consumo de Energía",
    "Peso Maquina": "Peso de Máquina",
}
# Crear styles.css
css_content = """
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    background-color: #f5f5f5;
}
h1 {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}
p.description {
    font-size: 16px;
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}
img {
    display: block;
    margin: 0 auto;
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
}
table {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
    border-collapse: collapse;
    background-color: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
th {
    background-color: #f2f2f2;
    font-weight: bold;
}
ul {
    list-style-type: none;
    padding: 0;
    text-align: center;
}
ul li {
    margin: 10px 0;
}
ul li a {
    text-decoration: none;
    color: #007bff;
    font-size: 18px;
}
ul li a:hover {
    text-decoration: underline;
}
.boton-vino {
    background-color: #7b1f31;
    color: white;
    padding: 12px 24px;
    font-size: 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    transition: background-color 0.3s ease;
}
.boton-vino:hover {
    background-color: #5c1624;
}
.centro {
    text-align: center;
    margin-top: 20px;
}
#tablaRepuestos {
    margin-top: 20px;
    text-align: center;
}
"""
with open(os.path.join(output_dir, "styles.css"), "w", encoding="utf-8") as f:
    f.write(css_content)
# Crear loader.js
loader_js_content = """
async function cargarRepuestos(jsonPath) {
    try {
        const response = await fetch(jsonPath);
        const data = await response.json();
        const repuestos = data.repuestos || [];
        const tabla = document.getElementById('tablaRepuestos');

        if (repuestos.length === 0) {
            tabla.innerHTML = '<p>No hay repuestos disponibles</p>';
            return;
        }

        tabla.innerHTML = `
            <table border="1" style="margin: 0 auto;">
                <tr><th>Repuesto</th><th>Código</th><th>Qty</th><th>UM</th></tr>
                ${repuestos.map(item => `
                    <tr>
                        <td>${item.Descripcion}</td>
                        <td>${item.Articulo}</td>
                        <td>${item.Cantidad}</td>
                        <td>${item.UM}</td>
                    </tr>
                `).join('')}
            </table>
        `;
        tabla.style.display = 'block';
    } catch (error) {
        console.error('Error loading repuestos:', error);
        document.getElementById('tablaRepuestos').innerHTML = '<p>Error al cargar los repuestos</p>';
    }
}
"""
with open(os.path.join(js_dir, "loader.js"), "w", encoding="utf-8") as f:
    f.write(loader_js_content)

# Plantilla HTML de activos
activo_template_path = os.path.join(templates_dir, "activo.html")
with open(activo_template_path, "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{{ nro_activo }} - Ficha Técnica</title>
    <link rel=\"stylesheet\" href=\"../../styles.css\">
</head>
<body>
    <img src=\"../../images/{{ nro_activo | replace(' ', '_') }}.webp\" alt=\"Imagen de {{ nro_activo }}\">
    <h1>{{ nro_activo }}</h1>
    <p class=\"description\">{{ descripcion }}</p>
    <table>
        <tr><th>Campo</th><th>Valor</th></tr>
        {% for key, value in datos.items() %}
        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
        {% endfor %}
    </table>

    {% if motor_data %}
    <img src=\"../../images/{{ motor_data.nro_activo | replace(' ', '_') }}.webp\" alt=\"Imagen de {{ motor_data.nro_activo }}\">
    <h1>{{ motor_data.nro_activo }}</h1>
    <p class=\"description\">{{ motor_data.descripcion }}</p>
    <table>
        <tr><th>Campo</th><th>Valor</th></tr>
        {% for key, value in motor_data.datos.items() %}
        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
        {% endfor %}
    </table>
    {% endif %}

    <div class=\"centro\">
        <button class=\"boton-vino\" onclick=\"cargarRepuestos('../../json_activos/{{ json_filename | replace(' ', '_') }}.json')\">Ver repuestos</button>
    </div>
    <div id=\"tablaRepuestos\"></div>
    <script src=\"../../js/loader.js\"></script>
</body>
</html>
""")

# Configurar Jinja2
env = Environment(loader=FileSystemLoader(templates_dir))
activo_template = env.get_template("activo.html")

# Agrupar por prefijos
csv_df = csv_df.dropna(subset=["Nro Activo"])
csv_df["Prefijo"] = csv_df["Nro Activo"].str.extract(r"^(\w+)")
prefijos_dict = csv_df.groupby("Prefijo")["Nro Activo"].apply(list).to_dict()

# Generar HTML por activo
for _, row in csv_df.iterrows():
    nro_activo = row["Nro Activo"]
    descripcion = row.get("Descripción", row.get("Descripcion", "Descripción no disponible"))
    activo_dir = os.path.join(activos_dir, nro_activo.replace(" ", "_"))
    os.makedirs(activo_dir, exist_ok=True)
    excluir = ["Activo Padre", "Nro Activo", "Descripción", "Descripcion", "Presion Operacion", "Alimentacion Electrica", "Potencia", "Prefijo"]
    datos = row.drop(labels=[col for col in excluir if col in row.index]).to_dict()
    datos_corregidos = {
        corrections.get(k, k): v for k, v in datos.items()
        if pd.notna(v) and str(v).strip() not in ("", "-")
    }

    base = "-".join(nro_activo.split("-")[:3])
    sufijos = ["-MT01", "-MB01", "-MB02"]
    motor_data = None
    for suf in sufijos:
        codigo_motor = base + suf
        fila_motor = excel_df[excel_df["ACTIVO"] == codigo_motor]
        if not fila_motor.empty:
            motor_row = fila_motor.iloc[0]
            motor_desc = motor_row.get("Descripción", "Descripción no disponible")
            motor_dict = motor_row.drop(labels=["ACTIVO", "Descripción"]).to_dict()
            motor_dict = {k: v for k, v in motor_dict.items() if pd.notna(v) and str(v).strip() not in ("", "-")}
            motor_data = {
                "nro_activo": codigo_motor,
                "descripcion": motor_desc,
                "datos": motor_dict
            }
            break

    json_filename = "-".join(nro_activo.split("-")[:2])

    html = activo_template.render(
        nro_activo=nro_activo,
        descripcion=descripcion,
        datos=datos_corregidos,
        motor_data=motor_data,
        json_filename=json_filename
    )
    with open(os.path.join(activo_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

# Generar index general agrupado por prefijo
index_html = """
<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Índice de Activos</title>
    <link rel='stylesheet' href='styles.css'>
</head>
<body>
    <h1>Índice de Activos por Prefijo</h1>
    {% for prefijo, activos in prefijos.items() %}
    <h2>{{ prefijo }}</h2>
    <ul>
        {% for activo in activos %}
        <li><a href='activos/{{ activo | replace(' ', '_') }}/index.html'>{{ activo }}</a></li>
        {% endfor %}
    </ul>
    {% endfor %}
</body>
</html>
"""
index_rendered = Environment().from_string(index_html).render(prefijos=prefijos_dict)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_rendered)

print("Generación completa con índice organizado por prefijo.")
