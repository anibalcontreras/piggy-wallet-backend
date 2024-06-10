import openai
import csv

# Configura tu clave de API
openai.api_key = "sk-proj-lMG0YGTdNOkWQhp3K3G9T3BlbkFJjW7V2xon9PuLiKNtrKPn"


# Definir la función de clasificación de texto
def clasificar_texto(texto):
    respuesta = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Utiliza el modelo adecuado
        messages=[
            {
                "role": "system",
                "content": "Eres un modelo que clasifica gastos en \
                categorías predefinidas.",
            },
            {
                "role": "user",
                "content": f"Clasifica el siguiente gasto en una de las \
              categorías: comida, transporte, vivienda, educación, salud, \
                 entretenimiento,\
             ahorro, inversión.\n\nTexto: {texto}\n\nCategoría:",
            },
        ],
        max_tokens=15,
        temperature=0,
    )
    categoría = respuesta.choices[0].message["content"].strip()
    return categoría


# Leer el archivo CSV y clasificar cada texto
gastos_clasificados = []
with open("AI/sets/gastos.csv", mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        texto = fila["gasto"]  # Asegurarse de leer la columna 'gasto'
        categoría = clasificar_texto(texto)
        gastos_clasificados.append({"id": fila["id"],
                                    "gasto": texto, "categoría": categoría})
        print(f"Texto: {texto}\nCategoría Predicha: {categoría}\n")


# Guardar las respuestas en un archivo CSV
with open("AI/sets/gastos_clasificados.csv", mode="w", encoding="utf-8",
          newline="") as archivo:
    fieldnames = ["id", "gasto", "categoría"]
    escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
    escritor.writeheader()
    escritor.writerows(gastos_clasificados)


# Definir la función de limpieza de categorías
def limpiar_categoria(categoria):
    # Eliminar el prefijo "categoría: " si está presente
    if categoria.lower().startswith("categoría: "):
        categoria = categoria[11:]
    # Eliminar el punto final si está presente
    if categoria.endswith("."):
        categoria = categoria[:-1]
    # Capitalizar la primera letra si está en minúscula
    categoria = categoria.capitalize()
    # Lista de categorías permitidas
    categorias_permitidas = [
        "Comida",
        "Transporte",
        "Vivienda",
        "Educación",
        "Salud",
        "Entretenimiento",
        "Ahorro",
        "Inversión",
    ]
    # Verificar si la categoría es permitida
    if categoria not in categorias_permitidas:
        raise ValueError(f"Categoría no permitida: {categoria}")
    return categoria


# Leer los datos del archivo CSV existente
gastos_clasificados = []
with open("AI/sets/gastos_clasificados.csv", mode="r",
          encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        gastos_clasificados.append(fila)

# Procesar cada categoría
for gasto in gastos_clasificados:
    try:
        gasto["categoría"] = limpiar_categoria(gasto["categoría"])
    except ValueError as e:
        print(e)

# Guardar las respuestas en un nuevo archivo CSV
with open("AI/sets/gastos_clasificados_procesados.csv", mode="w",
          encoding="utf-8", newline="") as archivo:
    fieldnames = ["id", "gasto", "categoría"]
    escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
    escritor.writeheader()
    escritor.writerows(gastos_clasificados)
