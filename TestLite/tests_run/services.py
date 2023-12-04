from itertools import zip_longest

from django.db import models, transaction

from tests.models import Test
from .models import TestRun, TestRunPrecondition, TestRunStep, TestRunPostcondition, ResultChoice, TypeOfRun

class TestRunServices:

    @classmethod
    def _fill_instance_of_data(cls, instance, position: int, test_run: models.Model, obj: models.Model):
        '''Заполняем модель для шагов выполнения теста'''
        record = obj()
        record.test_run = test_run
        record.action = instance['action']
        record.expected_result = instance['expected_result']
        record.position = position

        if instance['result'] == '':
            record.result = ResultChoice.PASSED
        else:
            record.result = instance['result']

        return record


    @classmethod
    def save_test_run(cls, test, user, start_time, preconditions, steps, postconditions):
        '''Метод сохраняет результаты выполнения теста в базу
        test_id - id теста который выполняется'''

        # Вычисляем самый приоритетный результат для всего тестового прогона на основе результата шагов
        priority_result = ResultChoice(max([ResultChoice(step['result']) for step in steps]))

        # Создаем тестовый прогон
        test_run = TestRun()
        test_run.test = test
        test_run.start_on = start_time
        test_run.type = TypeOfRun.MANUAL
        test_run.result = priority_result
        test_run.tester = user

        # Сохраняем тестовый прогон и его атрибуты в рамках одной транзакции
        with transaction.atomic():
            # Сохраянем тестовый прогон
            test_run.save()

            for i, (precondition, step, postcondition) in enumerate(zip_longest(preconditions, steps, postconditions)):
                if precondition is not None:
                    # Инициализируем предусловия
                    test_run_precondition = cls._fill_instance_of_data(precondition, i, test_run, TestRunPrecondition)
                    test_run_precondition.save()

                if step is not None:
                    # Инициализируем шаги
                    test_run_step = cls._fill_instance_of_data(step, i, test_run, TestRunStep)
                    test_run_step.save()

                if postcondition is not None:
                    # Инициализируем постусловия
                    test_run_postcondition = cls._fill_instance_of_data(postcondition, i, test_run, TestRunPostcondition)
                    test_run_postcondition.save()

            return test_run
