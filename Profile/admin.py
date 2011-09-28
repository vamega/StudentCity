from polls.models import Poll, Choice
from django.contrib import admin

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

class StudentAdmin(admin.ModelAdmin):  # Custom layout for the Poll admin page.
    list_display = ('name', 'email', 'rin')
    list_filter = ['name']
    search_fields = ['name']
    # fields = ['pub_date', 'question']  # This sets the order of the fields in the admin edit form.
    fieldsets = [  # This separates the fields into sections in the admin edit form.
        ('Name',               {'fields': ['first_name', 'middle_name', 'last_name']}),
        ('School Information', {'fields': ['rin', 'email', 'profile_picture_url']})
    ]
    inlines = [CourseInline]  # This adds the choices associated with the current Poll to the Poll form.
    
# To use custom settings, use the below lines:
admin.site.register(Student, StudentAdmin)

# To use default settings, use the below lines:
# admin.site.register(Poll)
# admin.site.register(Choice)
