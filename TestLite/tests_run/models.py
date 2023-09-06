from django.db import models



class ResultChoice(models.TextChoices):
    PASSED='Успешно'
    FAIL='Провал'
    ERROR='Ошибка'


class TypeOfRun(models.TextChoices):
    MANUAL='Ручное'
    AUTOMATED='Авто'


class TestRun(models.Model):
    '''Информация по прогону теста'''
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE)
    result = models.CharField(choices=ResultChoice.choices, max_length=6)
    type = models.CharField(choices=TypeOfRun.choices, default=TypeOfRun.MANUAL, max_length=10)

    start_on = models.DateTimeField()
    stop_on = models.DateField()



class TestPrecondition(models.Model):
    '''Информация о том как прошел данный шаг'''
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    