from django import forms
from bootstrap.forms import BootstrapForm, Fieldset


class RegistrationForm(BootstrapForm):
    '''
    A form to initiate the registration workflow.
    '''
    class Meta:
        layout = (
            Fieldset("Request a Scan",
                     "first_name",
                     "last_name",
                     "email_address",
                     "accepts_terms"),
            )

    first_name = forms.CharField(widget = forms.Textarea(attrs = {'rows' : 1, 'class' : 'span8'}))
    last_name = forms.CharField(widget = forms.Textarea(attrs = {'rows' : 1, 'class' : 'span8'}))
    email_address = forms.EmailField(widget = forms.Textarea(attrs = {'rows' : 1, 'class' : 'span8'}))
    accepts_terms = forms.BooleanField(required = True)

