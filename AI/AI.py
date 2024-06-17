# flake8: noqa
import openai
import os
from textwrap import dedent
from dotenv import load_dotenv


def setup_api_key():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(dotenv_path=env_path)
    openai.api_key = os.getenv("OPENAI_KEY")


def classify_text(texto):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": dedent(
                    """\
                    Eres un modelo que clasifica gastos en categorías predefinidas.
                """
                ),
            },
            {
                "role": "user",
                "content": dedent(
                    f"""\
                    Clasifica el siguiente gasto en una de las categorías: comida, transporte, vivienda, educación, salud, entretenimiento, ahorro, inversión.

                    Texto: {texto}

                    Categoría:
                """
                ),
            },
        ],
        max_tokens=15,
        temperature=0,
    )
    category = response["choices"][0]["message"]["content"].strip()
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


setup_api_key()
print(classify_text("Compré una pizza"))
print(clean_category(classify_text("Compré una pizza")))