from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


def invalid_name_validator(value):
    if 'invalid' in value:
        raise ValidationError('Это тестовое не валидируемое название')
    else:
        return value


class Test(models.Model):
    '''Основная информация по тестам'''
    class PriorityChoice(models.TextChoices):
        LOW = 'L', _('Низкий')
        MEDIUM = 'M', _('Средний')
        HIGH = 'H', _('Высокий')

    name = models.CharField(max_length=200, validators=[invalid_name_validator])
    description = models.TextField(validators=[invalid_name_validator])
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    priority = models.CharField(choices=PriorityChoice.choices, max_length=10)

    created_on = models.DateField(auto_now=True)
    modified_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tests:test_detail', kwargs={'id': self.id})
    


class TestPrecondition(models.Model):
    '''Предусловия для теста'''
    action = models.TextField(validators=[invalid_name_validator]) # Может больше или меньше
    expected_result = models.TextField(validators=[invalid_name_validator])
    position = models.IntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.test.name}: Precondition #{self.position}'



class TestStep(models.Model):
    '''Шаги которые включены в тест'''
    action = models.TextField(validators=[invalid_name_validator]) # Может больше или меньше
    expected_result = models.TextField(validators=[invalid_name_validator])
    position = models.IntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.test.name}: Step #{self.position}'
        



class TestPostcondition(models.Model):
    '''Постусловия для теста'''
    action = models.TextField(validators=[invalid_name_validator]) # Может больше или меньше
    expected_result = models.TextField(validators=[invalid_name_validator])
    position = models.IntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.test.name}: Postcondition #{self.position}'

    
