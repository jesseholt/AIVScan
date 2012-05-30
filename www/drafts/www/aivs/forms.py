from django import forms
from bootstrap.forms import BootstrapForm, Fieldset


class ScanRequestForm(BootstrapForm):
    '''
    A form to initiate the registration workflow.
    '''
    class Meta:
        layout = (
            Fieldset("Request a Scan",
                     "accepts_terms"),
            )

    accepts_terms = forms.BooleanField(label='I accept the Terms and Conditions',
                                       help_text = 'See the Terms and Conditions on this page.',
                                       error_messages={'required': 'You must accept the Terms and Conditions'})




