"""
Defines admin options for this RDFlib implementation.
"""
from rdflib.term import BNode

from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget

from . import fields, forms, models, store


@admin.register(models.NamedGraph)
class NamedGraphAdmin(admin.ModelAdmin):
    """
    Admin module for named graphs.
    """

    list_display = ('identifier', )
    ordering = ('identifier', )
    search_fields = ('identifier', )


@admin.register(models.NamespaceModel)
class NamespaceAdmin(admin.ModelAdmin):
    """
    Admin module for managing namespaces.
    """
    list_display = ('store', 'prefix', 'uri')
    list_display_links = ('prefix',)
    ordering = ('-store', 'prefix')
    search_fields = ('prefix', 'uri')
    form = forms.NamespaceForm

    def get_actions(self, request):
        return []

    def has_delete_permission(self, request, obj=None):
        """
        Default namespaces cannot be deleted.
        """
        if obj is not None and obj.store == store.DEFAULT_STORE:
            return False

        return super(NamespaceAdmin, self).has_delete_permission(request, obj)


class AdminURIWidget(AdminTextareaWidget):

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a form.
        """
        # test below shouldn't be necessary if code in fields module was more coherent
        if isinstance(value, BNode):
            return fields.serialize_uri(value)
        else:
            return value


@admin.register(models.URIStatement)
class UriStatementAdmin(admin.ModelAdmin):
    """
    Admin module for URI statements.
    """
    ordering = ('context', 'subject', 'predicate')
    search_fields = ('subject', 'predicate', 'object')
    list_per_page = 100
    formfield_overrides = {
       fields.URIField: {'widget': AdminURIWidget()},
    }


class AdminLiteralWidget(AdminTextareaWidget):

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a form.
        """
        if value is None:
            return None
        return "{}^^{}^^{}".format(
            value, value.language or '', value.datatype or ''
        )


@admin.register(models.LiteralStatement)
class LiteralStatementAdmin(admin.ModelAdmin):
    """
    Admin module for literal statements.
    """
    ordering = ('context', 'subject', 'predicate')
    search_fields = ('subject', 'predicate', 'object')
    list_per_page = 100
    formfield_overrides = {
       fields.URIField: {'widget': AdminURIWidget()},
       fields.LiteralField: {'widget': AdminLiteralWidget()},
    }
