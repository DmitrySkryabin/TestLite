from TestLite.utils import query_debugger
from .models import Test, TestPostcondition, TestPrecondition, TestStep


class Return:
    '''Класс для возврата элементов в view'''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)



class TestServices():
    '''Сервисы для обработки данных тестов'''
    @query_debugger
    def get_all_test_attributes(id) -> dict:
        '''Возвращает все что связано с конкретным тестом'''
        test = Test.objects.get(id=id)

        test_postconditions = TestPostcondition.objects.filter(test=test).all()
        test_preconditions = TestPrecondition.objects.filter(test=test).all()
        test_steps = TestStep.objects.filter(test=test).all()

        return Return(
            test = test,
            test_postconditions = test_postconditions,
            test_preconditions = test_preconditions,
            test_steps = test_steps
        )