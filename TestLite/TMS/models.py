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


class Project(models.Model):
    '''Проект к которому привязаны все тест кейсы'''
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class BaseTestStep(models.Model):
    '''Абстрактная модель для шагов теста'''
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
    postconditions = models.TextField() # Постусловия
    priority = models.CharField(choices=PRIORITY, max_length=20)
    parameters = models.JSONField() # Данные для тестов
    version = models.IntegerField()

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'



class TestStep(BaseTestStep):
    '''Модель с шагами тест кейса'''
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_case}:{self.pk}'



class TestCaseRun(models.Model):
    '''Модель с запуском тест кейса'''
    # name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.FloatField()
    type = models.TextField(choices=TYPE, max_length=20) # Тип запуска 
    status = models.TextField(choices=STATUS, max_length=50)

    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_case}:{self.pk}::{self.status}'



class TestStepRun(BaseTestStep):
    '''Модель с выполненными шагами'''
    result = models.CharField(choices=STATUS, max_length=50)
    test_case_run = models.ForeignKey(TestCaseRun, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_case_run}:{self.pk}'



class TestSuite(models.Model):
    '''Тестовый суит с тест кейсами'''
    name = models.CharField(max_length=200)
    description = models.TextField()

    test_cases = models.ManyToManyField(TestCase)

    def __str__(self):
        return f'{self.name}'



class TestSuiteRun(models.Model):
    '''Модель с информацией по выполненному тест суиту'''
    # name = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS, max_length=50)

    test_suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_suite}:{self.pk}::{self.status}'
    