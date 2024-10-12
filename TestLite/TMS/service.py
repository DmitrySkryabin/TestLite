from .models import TestCase, TestCaseRun, TestStep, TestStepRun, TestSuite, TestSuiteRun, TYPE, STATUS


class TestSuiteSaveHelper:

    @classmethod
    def save_test_suite_run(cls, testsuite_key, data, type=TYPE.AUTO):
        testsuite = TestSuite.objects.get(key=testsuite_key)
        testcases = testsuite.test_cases.all()

        # Создаем тест суит ран
        testsuite_run = TestSuiteRun()
        testsuite_run.type = type
        testsuite_run.status = STATUS.PASSED
        testsuite_run.test_suite = testsuite
        testsuite_run.save()

        min_status = STATUS.SKIP

        # Создаем тест кейс ран
        for testrun in data:
            testcase_run = TestCaseRun()
            testcase_run.start_time = testrun['startime_readable']
            testcase_run.stop_time = testrun['stoptime_readable']
            testcase_run.duration = testrun['duration']
            testcase_run.type = TYPE.AUTO
            testcase_run.status = STATUS[testrun['status'].upper()]
            if testrun['precondition_status'] is not None:
                testcase_run.precondition_status = STATUS[testrun['precondition_status'].upper()] 
            if testrun['postcondition_status'] is not None:
                testcase_run.postcondition_status = STATUS[testrun['postcondition_status'].upper()] 
            testcase_run.log = testrun['log']
            testcase_run.report = testrun['report']
            testcase_run.skipreason = testrun['skipreason']
            testcase_run.test_case = TestCase.objects.get(key=testrun['testcase_key'])
            testcase_run.test_suite_run = testsuite_run
            testcase_run.save()

            if testcase_run.status.its_more_important(min_status):
                min_status = testcase_run.status

            # Создаем тест степ ран
            for id, teststep in enumerate(TestStep.objects.filter(test_case=testcase_run.test_case), start=1):
                teststep_run = TestStepRun()
                teststep_run.action = teststep.action
                teststep_run.expected_result = teststep.expected_result
                teststep_run.test_case_run = testcase_run
                
                if testcase_run.status != STATUS.SKIP:
                    if testrun['step_number_with_error'] is not None:
                        if id == testrun['step_number_with_error']:
                            teststep_run.result = STATUS.FAIL
                        if id < testrun['step_number_with_error']:
                            teststep_run.result = STATUS.PASSED
                        if id > testrun['step_number_with_error']:
                            teststep_run.result = STATUS.SKIP
                    else:
                        teststep_run.result = STATUS.PASSED
                else:
                    teststep_run.result = STATUS.SKIP
                teststep_run.save()

        testsuite_run.status = min_status
        testsuite_run.save()



