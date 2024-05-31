import openai
import csv

# Configura tu clave de API
openai.api_key = 'sk-proj-lMG0YGTdNOkWQhp3K3G9T3BlbkFJjW7V2xon9PuLiKNtrKPn'

import openai
import csv

# Definir la función de clasificación de texto
def clasificar_texto(texto):
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Utiliza el modelo adecuado
        messages=[
            {"role": "system", "content": "Eres un modelo que clasifica gastos en categorías predefinidas."},
            {"role": "user", "content": f"Clasifica el siguiente gasto en una de las categorías: comida, transporte, vivienda, educación, salud, entretenimiento, ahorro, inversión.\n\nTexto: {texto}\n\nCategoría:"}
        ],
        max_tokens=15,
        temperature=0
    )
    categoría = respuesta.choices[0].message['content'].strip()
    return categoría

# Leer el archivo CSV y clasificar cada texto
gastos_clasificados = []
with open('AI/sets/gastos.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        texto = fila['gasto']  # Asegurarse de leer la columna 'gasto'
        categoría = clasificar_texto(texto)
        gastos_clasificados.append({"id": fila["id"], "gasto": texto, "categoría": categoría})
        print(f'Texto: {texto}\nCategoría Predicha: {categoría}\n')

# Guardar las respuestas en un archivo CSV
with open('AI/sets/gastos_clasificados.csv', mode='w', encoding='utf-8', newline='') as archivo:
    fieldnames = ["id", "gasto", "categoría"]
    escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
    escritor.writeheader()
    escritor.writerows(gastos_clasificados)

print("Archivo gastos_clasificados.csv generado con éxito.")

# Ejemplo de clasificación directa
texto_ejemplo = "Compré una hamburguesa en el almuerzo"
categoría_predicha = clasificar_texto(texto_ejemplo)
print(f'Texto: {texto_ejemplo}\nCategoría Predicha: {categoría_predicha}\n')
