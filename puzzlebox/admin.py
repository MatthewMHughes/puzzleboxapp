from django.contrib import admin

from .models import Dial

class DialOneInline(admin.TabularInline):
    model = Dial,
    fk_name = "dial_one"

class DialTwoInline(admin.TabularInline):
    model = Dial,
    fk_name = "dial_two"

class DialAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["dialPosition", "pistonPosition", "dialCenter", "firstLinkDir", "secondLinkDir"]}),
    ]
    #list_display = ["dialPosition"]
    #list_filter = ["dialPosition"]
    #search_fields = ["dialPosition"]
    #inlines = [DialOneInline, DialTwoInline]
admin.site.register(Dial)