"""
Base forms for editing the models in this module.
You can use or extend these forms in your
project to ensure that all validation is correct.
"""
from rdflib import namespace

from django import forms

from . import models


class NamespaceForm(forms.ModelForm):
    """
    Form for editing namespaces.
    """

    class Meta:
        model = models.NamespaceModel
        fields = ('prefix', 'uri')

    def clean_prefix(self):
        """
        Validates the prefix
        """
        prefix = self.cleaned_data['prefix']
        if not namespace.is_ncname(prefix):
            raise forms.ValidationError("This is an invalid prefix")

        return prefix

    def clean_uri(self):
        """
        Validates the URI
        """
        uri = self.cleaned_data['uri']
        # todo: URI validation
        return uri
