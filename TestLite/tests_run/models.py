from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _



def invalid_name_validator(value):
    if 'invalid' in value:
        raise ValidationError('Это тестовое не валидируемое название')
    else:
        return value


def result_choice_gt(value1, value2):
    ordering = [
        ResultChoice.BLOCKED[0],
        ResultChoice.PASSED[0],
        ResultChoice.FAIL[0],
        ResultChoice.ERROR[0]
    ]
    if ordering.index(value1) > ordering.index(value2):
        return True
    else:
        return False


class ResultChoice(models.TextChoices):
    PASSED = 'P', _('Успешно')
    FAIL = 'F', _('Провал')
    ERROR = 'E', _('Ошибка')
    BLOCKED = 'B',_('Заблокирован')

    
    def __lt__(self, other):
        if not isinstance(other, (str, ResultChoice)):
            raise TypeError("Правый операнд должен быть str или ResultChoice")
        print('IST __lt__')
        ordering = [self.BLOCKED[0], self.PASSED[0], self.FAIL[0], self.ERROR[0]]
        print(f'self: {self} index: {ordering.index(self)}')
        print(f'other: {other} index: {ordering.index(other)}')
        return ordering.index(self) < ordering.index(other if isinstance(other, str) else other.value)


    
    # def __gt__(self, other):
    #     if isinstance(other, ResultChoice):
    #         if self.__ordering.index(self.value) < self.__ordering.index(self.value):
    #             return False
    #         else:
    #             return True
            

    # def __eq__(self, other):
    #     if isinstance(other, ResultChoice):
    #         if self.__ordering.index(self.value) == self.__ordering.index(self.value):
    #             return True
    #         else:
    #             return False



class TypeOfRun(models.TextChoices):
    MANUAL = 'M', _('Ручное')
    AUTOMATED = 'A', _('Авто')


class TestRun(models.Model):
    '''Информация по прогону теста'''
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE)
    result = models.CharField(choices=ResultChoice.choices, max_length=10)
    type = models.CharField(choices=TypeOfRun.choices, default=TypeOfRun.MANUAL, max_length=20)
    tester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    start_on = models.DateTimeField()
    stop_on = models.DateTimeField(auto_now=True)



class TestRunPrecondition(models.Model):
    '''Информация о том как прошел данный шаг (предусловие)'''
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    #test_precondition = models.ForeignKey('tests.TestPrecondition', on_delete=models.SET_NULL, null=True)

    action = models.TextField(validators=[invalid_name_validator])
    expected_result = models.TextField()
    position = models.IntegerField()

    result = models.CharField(choices=ResultChoice.choices, max_length=10)



class TestRunStep(models.Model):
    '''Информация о том как прошел данный шаг (Шаг)'''
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    #test_step = models.ForeignKey('tests.TestStep', on_delete=models.SET_NULL, null=True)

    action = models.TextField()
    expected_result = models.TextField()
    position = models.IntegerField()

    result = models.CharField(choices=ResultChoice.choices, max_length=10)



class TestRunPostcondition(models.Model):
    '''Информация о том как прошел данный шаг (Постусловие)'''
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    #test_postcondition = models.ForeignKey('tests.TestPostcondition', on_delete=models.SET_NULL, null=True)

    action = models.TextField()
    expected_result = models.TextField()
    position = models.IntegerField()

    result = models.CharField(choices=ResultChoice.choices, max_length=10)