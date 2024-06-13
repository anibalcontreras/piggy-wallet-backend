import openai
import os


def setup_api_key():
    openai.api_key = os.environ["OPENAI_KEY"]


def classify_text(texto):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
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
    category = response.choices[0].message["content"].strip()
    return category


def clean_category(category):
    if category.lower().startswith("categoría: "):
        category = category[11:]
    if category.endswith("."):
        category = category[:-1]
    category = category.capitalize()
    categories_allowed = [
        "Comida",
        "Transporte",
        "Vivienda",
        "Educación",
        "Salud",
        "Entretenimiento",
        "Ahorro",
        "Inversión",
    ]
    if category not in categories_allowed:
        raise ValueError(f"Categoría no permitida: {category}")
    return category
