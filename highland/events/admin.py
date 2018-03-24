from django.contrib import admin
from django import forms
from django.contrib.admin.filterspecs import FilterSpec, DateFieldFilterSpec
from .models import Event, EventType, NewsItem
import datetime

class MyDateSpec(DateFieldFilterSpec):

    def title(self):
        return "Year"

    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(MyDateSpec, self).__init__(f, request, params, model,
                                               model_admin, field_path=field_path)
        self.request = request
        self.current_year = datetime.datetime.now().year
	self.year_list = [self.current_year + 1, self.current_year,
                          self.current_year - 1, self.current_year-2]

    def choices(self, cl):

        selected_year = None

        for year in self.year_list:
            if self.request.GET.get(str(year), None):
                selected_year = year

            range_start = '%s-01-01' % str(year)
            range_stop = '%s-12-31' % str(year)
         
            yield {'selected': self.request.GET.get(str(year), None) == 'True',
                'query_string': cl.get_query_string(
                                {'start_date__gte': range_start,
                                 'start_date__lte': range_stop},
                                ['start_date']),
                'display': str(year)}

        yield {'selected': not(selected_year),
               'query_string': cl.get_query_string(
                               {},
                               ['start_date']),
               'display': 'All'}


FilterSpec.filter_specs.insert(0, (lambda f: f.name == 'start_date', MyDateSpec))

class EventAdmin(admin.ModelAdmin):

    list_display = ('event_title', 'event_desc', 'start_date', 'start_time', 'end_time', 'event_type')
    list_filter = ('start_date',)
    ordering = ('-start_date',)

class EventTypeAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('id', 'event_type_desc')
    ordering = ('id',)

class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'news_title', 'news_date', 'news_long', 'news_image', 'added_date')
    ordering = ('-news_date',)
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(NewsItemAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'news_long':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(NewsItem, NewsItemAdmin)

