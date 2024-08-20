from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Create your models here.
class STATUS(models.TextChoices):
    PASSED = 'P', _('Успешно')
    SKIPED = 'S', _('Пропущено')
    ERROR = 'E', _('Ошибка')
    FAIL = 'F', _('Провал')


class PRIORITY(models.TextChoices):
    LOW = 'L', _('Низкий')
    MEDIUM = 'M', _('Средний')
    HIGH = 'H', _('Высокий')


class TYPE(models.TextChoices):
    MANUAL = 'M', _('Ручной')
    AUTO = 'A', _('Авто')



class BaseTestStep(models.Model):
    action = models.TextField()
    expected_result = models.TextField()
    position = models.IntegerField()

    class Meta:
        abstract = True


class TestCase(models.Model):
    '''Модель тест кейса'''
    name = models.CharField(max_length=200)
    description = models.TextField()
    preconditions = models.TextField() # Предусловия
    pastconditions = models.TextField() # Постусловия
    priority = models.CharField(choices=PRIORITY, max_length=20)
    parameters = models.JSONField() # Данные для тестов
    version = models.IntegerField()

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)



class TestStep(BaseTestStep):
    '''Модель с шагами тест кейса'''
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)



class TestCaseRun(models.Model):
    '''Модель с запуском тест кейса'''
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.FloatField()
    type = models.TextField(choices=TYPE, max_length=20) # Тип запуска 
    status = models.TextField(choices=STATUS, max_length=50)

    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)



class TestStepRun(BaseTestStep):
    test_case_run = models.ForeignKey(TestCaseRun, on_delete=models.CASCADE)



class TestSuite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    test_cases = models.ManyToManyField(TestCase)



class TestSuiteRun(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS, max_length=50)

    test_suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)