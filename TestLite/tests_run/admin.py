from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TestRunSuite)
admin.site.register(TestRun)
admin.site.register(TestRunPrecondition)
admin.site.register(TestRunStep)
admin.site.register(TestRunPostcondition)
