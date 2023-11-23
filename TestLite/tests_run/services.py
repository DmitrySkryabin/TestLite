from datetime import datetime
from itertools import zip_longest

from django.db import models

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
    def save_test_run(cls, test_id: int, user, preconditions, steps, postconditions):
        '''Метод сохраняет результаты выполнения теста в базу
        test_id - id теста который выполняется'''

        # Вычисляем самый приоритетный результат для всего тестового прогона на основе результата шагов
        priority_result = ResultChoice(max([ResultChoice(step['result']) for step in steps]))

        # Создаем тестовый прогон
        test_run = TestRun()
        test_run.test = Test.objects.get(id=test_id)
        test_run.start_on = datetime.now()
        test_run.type = TypeOfRun.MANUAL
        test_run.result = priority_result
        test_run.tester = user

        test_run.save()

        # calculated_result = ResultChoice.BLOCKED

        # test_run_preconditions = []
        # test_run_steps = []
        # test_run_postconditions = []
        
        # for step in steps:
        #     if calculated_result.its_bellow(step.result):
        #         calculated_result = ResultChoice(step.result)


        for i, precondition, step, postcondition in enumerate(zip_longest(preconditions, steps, postconditions)):
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

        # for i, instance in enumerate(preconditions):
        #     test_run_precondition = self.fill_instance_of_data(instance, i, TestRunPrecondition)
        #     test_run_precondition.test_run = test_run
        #     test_run_preconditions.append(test_run_precondition)

        # for i, instance in enumerate(steps):
        #     test_run_step = self.fill_instance_of_data(instance, i, TestRunStep)
        #     test_run_step.test_run = test_run
        #     test_run_steps.append(test_run_step)

        #     if calculated_result.its_bellow(test_run_step.result):
        #         calculated_result = ResultChoice(test_run_step.result)

        # for i, instance in enumerate(postconditions):
        #     test_run_postcondition = self.fill_instance_of_data(instance, i, TestRunPostcondition)
        #     test_run_postcondition.test_run = test_run
        #     test_run_postconditions.append(test_run_postcondition)
