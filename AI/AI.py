import openai
import csv

# Configura tu clave de API
openai.api_key = 'sk-proj-lMG0YGTdNOkWQhp3K3G9T3BlbkFJjW7V2xon9PuLiKNtrKPn'

# Función para clasificar texto
def clasificar_texto(texto):
    respuesta = openai.Completion.create(
      engine="gpt-3.5-turbo-1106",  # Asegúrate de utilizar el motor adecuado
      prompt=f"Clasifica el siguiente gasto en una de las categorías: comida, transporte, vivienda, educación, salud, entretenimiento, ahorro, inversión.\n\nTexto: {texto}\n\nCategoría:",
      max_tokens=10,
      temperature=0
    )
    categoría = respuesta.choices[0].text.strip()
    return categoría

# Leer el archivo CSV y clasificar cada texto
with open('AI/gastos.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        texto = fila['texto']
        categoría = clasificar_texto(texto)
        print(f'Texto: {texto}\nCategoría Predicha: {categoría}\n')

# Ejemplo de clasificación directa
texto_ejemplo = "Compré una hamburguesa en el almuerzo"
categoría_predicha = clasificar_texto(texto_ejemplo)
print(f'Texto: {texto_ejemplo}\nCategoría Predicha: {categoría_predicha}\n')
