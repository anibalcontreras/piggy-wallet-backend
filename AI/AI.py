# flake8: noqa
import openai
import os
from textwrap import dedent
from dotenv import load_dotenv
from categories.models import Category
from categories.exceptions import InvalidCategoryError


GPT_MODEL = "gpt-4-turbo"


def get_category_name_from_description(description):
    classified_category = classify_text(description)
    cleaned_category = category_matched_with_id(classified_category)

    if not Category.objects.filter(name=cleaned_category).exists():
        raise ValueError("Categoría no encontrada.")
    return cleaned_category


def classify_text(texto):
    setup_api_key()
    if not openai.api_key:
        raise ValueError("OpenAI API key is not set. Please check your .env file.")

    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
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


def setup_api_key():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(dotenv_path=env_path)
    openai.api_key = os.getenv("OPENAI_KEY")


def category_matched_with_id(category):
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
        raise InvalidCategoryError(category)
    return category
