from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
import django_tables2 as tables
from django.db import models
import django_filters as filters
from crispy_forms.helper import FormHelper
from django.views.generic import CreateView, UpdateView


class CustomUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.title
        context['cancel_url'] = self.cancel_url
        return context


class CustomCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.title
        context['cancel_url'] = self.cancel_url
        return context


class PageFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        def get_filterset_class(self):
            attrs = dict()
            attrs['Meta'] = type('Meta', (), {'fields': self.filter_fields, 'model': self.model})
            klass1 = type('Dfilter', (filters.FilterSet,), attrs)
            return klass1

        def get_form_class(self):
            attrs = dict()
            attrs['model'] = self.model
            attrs['form_tag'] = False
            attrs['help_text_inline'] = True
            attrs['form_class'] = 'form-horizontal'
            klass1 = type('Dform', (FormHelper,), attrs)
            return klass1

        qs = super().get_queryset()
        self.formhelper_class = get_form_class(self)
        self.filter_class = get_filterset_class(self)

        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context[self.context_filter_name] = self.filter
        return context


class AddTableMixin(object, ):
    table_pagination = {"per_page": 15}

    def get_table_class(self):
        def get_table_column(field):
            if isinstance(field, models.DateTimeField):
                return tables.DateColumn("d/m/y H:i")
            else:
                return tables.Column()

        attrs = dict(
            (field.name, get_table_column(field)) for
            field in self.model._meta.fields if field.name not in self.exclude
        )

        metaAttrs = dict()
        metaAttrs['class'] = 'table'
        if hasattr(self, 'actions'):
            metaAttrs['actions'] = self.actions
        if hasattr(self, 'title'):
            metaAttrs['title'] = self.title
        if hasattr(self, 'add_link'):
            metaAttrs['add_link'] = self.add_link

        attrs['Meta'] = type('Meta', (), {'attrs': metaAttrs})
        klass = type('Dtable', (tables.Table,), attrs)
        return klass
