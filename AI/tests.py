# flake8: noqa
import unittest
from unittest.mock import patch
from AI import classify_text, category_matched_with_id
from textwrap import dedent
from categories.exceptions import InvalidCategoryError


class TestGastosClassifier(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_classify_text(self, mock_create):
        # Configurar el mock para devolver una respuesta simulada
        mock_create.return_value = {"choices": [{"message": {"role": "assistant", "content": "Comida."}}]}

        # Llamar a la función a probar
        texto = "Compré una pizza."
        categoria = classify_text(texto)

        # Verificar que la respuesta sea la esperada
        self.assertEqual(categoria, "Comida.")

        # Verificar que la API fue llamada con los parámetros correctos
        mock_create.assert_called_once_with(
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

    def test_clean_category(self):
        # Pruebas con diferentes casos
        self.assertEqual(category_matched_with_id("Categoría: Comida."), "Comida")
        self.assertEqual(category_matched_with_id("categoría: transporte"), "Transporte")
        self.assertEqual(category_matched_with_id("vivienda."), "Vivienda")

        # Prueba de una categoría no permitida
        with self.assertRaises(InvalidCategoryError):
            category_matched_with_id("Categoría: Viajes.")


if __name__ == "__main__":
    unittest.main()
