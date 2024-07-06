class InvalidCategoryError(Exception):
    def __init__(self, category):
        self.category = category
        self.message = (
            "El texto proporcionado no proporciona información suficiente para "
            "clasificar el gasto en una categoría. Por favor, se un poco mas descriptivo."
        )
        self.code = 400
        super().__init__(self.message)
