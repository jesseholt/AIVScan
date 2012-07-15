from django import forms
from bootstrap.forms import BootstrapForm, Fieldset


class ScanRequestForm(BootstrapForm):
    '''
    A mini-form to initiate the scanner workflow.
    '''
    class Meta:
        layout = (
            Fieldset("Request a Scan",
                     "accepts_terms"),
            )

    accepts_terms = forms.BooleanField(label='I accept the Terms and Conditions',
                                       help_text = 'See the Terms and Conditions on this page.',
                                       error_messages={'required': 'You must accept the Terms and Conditions'})


class ContactForm(BootstrapForm):
    '''
    A form to initiate the registration workflow.
    '''
    class Meta:
        layout = (
            Fieldset('ContactUs',
                     'email_address',
                     'email_verify',
                     'message'),
            )

    email_address = forms.EmailField( label = 'Email Address',
                                      initial = 'Enter your email address',
                                      widget = forms.TextInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                                      help_text = 'Your valid email address, up to 200 characters.',
                                      error_messages = { 'required': 'You must supply an email address.',
                                                         'invalid': 'That does not appear to be a valid email address.',
                                                         'max_length': 'A maximum of 200 characters, please.'},
                                      max_length=200)

    email_verify = forms.EmailField( label = 'Verify Email',
                                      initial = 'Enter your email address',
                                      widget = forms.TextInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                                      help_text = 'Your valid email address, up to 200 characters.',
                                      error_messages = { 'required': 'You must confirm your email address.',
                                                         'invalid': 'That does not appear to be a valid email address.',
                                                         'max_length': 'A maximum of 200 characters, please.'},
                                      max_length=200)

    message = forms.CharField( label = 'Message',
                                  initial = 'Enter a message here.',
                                  widget = forms.Textarea(attrs = {'rows' : 6, 'class' : 'span4 input-large'}),
                                  help_text = 'Your message here.',
                                  error_messages = { 'required': 'You must supply a message.',
                                                     'max_length': 'A maximum of 10000 characters, please.'},
                               max_length=10000)

    def clean_email_address(self):
        '''
        Verifies that the email addresses provided match.
        complexity.
        '''
        candidate = self.data['email_address']
        if candidate != self.data['email_verify']:
            raise forms.ValidationError('These email addresses don\'t match.  Please try again.')
        return candidate

