from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TestCase)
admin.site.register(TestStep)
admin.site.register(TestCaseRun)
admin.site.register(TestStepRun)
admin.site.register(TestSuite)
admin.site.register(TestSuiteRun)

