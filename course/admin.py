from django.contrib import admin
from mce_filebrowser.admin import MCEFilebrowserAdmin
from .models import Author, Category, Bank, Account, Location, Course, Training, Member, Register, Booking

class CourseAdmin(MCEFilebrowserAdmin):

	def get_form(self, request, obj=None, **kwargs):
		form = super(CourseAdmin, self).get_form(request, obj=None, **kwargs)
		form.base_fields['authors'].help_text = ''
		form.base_fields['accounts'].help_text = ''
		return form

	fieldsets = (
		(None, {'fields': ('code', 'name', 'description', 'image', 'tags',)}),
		('Properties', {'fields': ('category', 'authors', 'level', 'lessons', 'hours', 'price',)}),
		('Payment', {'fields': ('accounts',)}),
		('Publish', {'fields': ('is_hot', 'is_publish',)}),
		('Statistics', {'fields': ('views', 'rating',), 'classes': ('collapse',)}),
	)
	readonly_fields = ('views', 'rating',)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Location)
admin.site.register(Course, CourseAdmin)
admin.site.register(Training)
admin.site.register(Member)
admin.site.register(Register)
admin.site.register(Booking)
