from django.contrib import admin
from .models import Vuln, Remedy

admin.site.register(Vuln)
admin.site.register(Remedy)
