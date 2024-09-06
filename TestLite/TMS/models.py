from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Create your models here.
class STATUS(models.TextChoices):
    PASSED = 'P', _('Успешно')
    SKIPED = 'S', _('Пропущено')
    ERROR = 'E', _('Ошибка')
    FAIL = 'F', _('Провал')

    def __get_order(self):
        return {
            STATUS.SKIPED[0]: 0,
            STATUS.PASSED[0]: 1,
            STATUS.FAIL[0]: 2,
            STATUS.ERROR[0]: 3
        }

    def its_more_important(self, other):
        '''
        Метод для проверки значимости результата 
        Так, например, результат ERROR приоритетнее чем FAIL
        Возвращает True если other больше
        '''
        order = self.__get_order()
        return order[self] > order[other]
    

    @classmethod
    def get_object(cls, key):
        for item in cls:
            if str(item) == key:
                return item



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

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    

    def get_status_display(self):
        status = TestCaseRun.objects.filter(test_case=self).last().status
        return [choice for choice in STATUS.choices if choice[0] == status][0][1]



class TestStep(BaseTestStep):
    '''Модель с шагами тест кейса'''
    position = models.IntegerField()
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_case}:{self.pk}'
    

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
    type = models.CharField(choices=TYPE, max_length=20)
    status = models.CharField(choices=STATUS, max_length=50)
    date_time = models.DateTimeField(auto_now=True)

    test_suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_suite}:{self.pk}::{self.status}'
    

class TestCaseRun(models.Model):
    '''Модель с запуском тест кейса'''
    # name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.FloatField()
    type = models.CharField(choices=TYPE, max_length=20) # Тип запуска 
    status = models.CharField(choices=STATUS, max_length=50)

    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    test_suite_run = models.ForeignKey(TestSuiteRun, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_case}:{self.pk}::{self.status}'
    

    def get_test_steps(self):
        return TestStepRun.objects.filter(test_case_run=self)

    

class TestStepRun(BaseTestStep):
    '''Модель с выполненными шагами'''
    # action = models.TextField()
    # expected_result = models.TextField()
    result = models.CharField(choices=STATUS, max_length=50)
    test_case_run = models.ForeignKey(TestCaseRun, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.test_case_run}:{self.pk}'
    
    