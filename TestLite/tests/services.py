from .models import Test, TestPostcondition, TestPrecondition, TestStep


class TestServices():
    '''Сервисы для обработки данных тестов'''
    
    def get_all_test_attributes(id) -> dict:
        '''Возвращает все что связано с конкретным тестом'''
        test = Test.objects.get(id=id)

        # test_postconditions = TestPostcondition.objects.filter(test=test)
        # test_preconditions = TestPrecondition.objects.filter(test=test)
        # test_steps = TestStep.objects.filter(test=test)

        # data = {
        #     'test': test,
        #     'test_postconditions': test_postconditions,
        #     'test_preconditions': test_preconditions,
        #     'test_steps': test_steps
        # }

        return test