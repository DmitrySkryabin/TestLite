from django.core.exceptions import ValidationError

class TestCaseInnerValidator:

    def __call__(self, value):
        if not isinstance(value, list):
            raise ValidationError("Поле 'steps' должно быть списком.")
        
    def deconstruct(self):
        path = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return (path, (), {})