from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Test(models.Model):
    '''Основная информация по тестам'''
    class PriorityChoice(models.TextChoices):
        LOW = 'Низкий'
        MEDIUM = 'Средний'
        HIGH = 'Высокий'

    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(choices=PriorityChoice.choices, max_length=10)

    created_on = models.DateField(default=timezone.now)
    modified_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name



class TestPrecondition(models.Model):
    '''Предусловия для теста'''
    action = models.CharField(max_length=500) # Может больше или меньше
    expected_result = models.TextField()
    position = models.IntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.test.name}: Precondition #{self.position}'



class TestStep(models.Model):
    '''Шаги которые включены в тест'''
    action = models.CharField(max_length=500) # Может больше или меньше
    expected_result = models.TextField()
    position = models.IntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.test.name}: Step #{self.position}'
        



class TestPostcondition(models.Model):
    '''Постусловия для теста'''
    action = models.CharField(max_length=500) # Может больше или меньше
    expected_result = models.TextField()
    position = models.IntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.test.name}: Postcondition #{self.position}'

    
