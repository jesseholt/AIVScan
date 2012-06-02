from django import forms
from bootstrap.forms import BootstrapForm, Fieldset


class AuthenticationForm(BootstrapForm):
    '''
    A form to log the user in.
    '''
    class Meta:
        layout = (
            Fieldset("Log In",
                     'email_address',
                     'password'),
            )

    email_address = forms.EmailField( label = 'Email Address',
                                      initial = 'Enter your email address',
                                      widget = forms.Textarea(attrs = {'rows' : 1, 'class' : 'span6'}),
                                      help_text = 'Your valid email address, up to 200 characters.',
                                      error_messages = { 'required': 'You must supply an email address.',
                                                         'invalid': 'That does not appear to be a valid email address.',
                                                         'max_length': 'A maximum of 200 characters, please.'},
                                      max_length=200)

    password = forms.CharField(label = 'Password',
                               initial = 'Enter your password',
                               widget = forms.PasswordInput(attrs = {'rows' : 1, 'class' : 'span6'}),
                               help_text = 'Pick a strong password between 8 and 30 characters long.',
                               error_messages={'required': 'You must choose a password',
                                               'max_length':
                                               'That is an awfully long password!  A max of 30 characters, please!',
                                               'min_length':
                                               'Choose a longer password.  A minimum of 8 characters, please.'},
                               min_length=8,
                               max_length=30)


class RegistrationForm(BootstrapForm):
    '''
    A form to initiate the registration workflow.
    '''
    class Meta:
        layout = (
            Fieldset("Register",
                     "first_name",
                     "last_name",
                     "email_address",
                     'password',
                     'password_verify',
                     "accepts_terms"),
            )

    first_name = forms.CharField( label = 'First Name',
                                  initial = 'Enter your first name',
                                  widget = forms.TextInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                                  help_text = 'Your first name, up to 30 characters',
                                  error_messages = { 'required': 'You must supply your first name.',
                                                     'max_length': 'A maximum of 30 characters, please.'},
                                  max_length=30)

    last_name = forms.CharField( label = 'Last Name',
                                  initial = 'Enter your last name',
                                  widget = forms.TextInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                                  help_text = 'Your last name, up to 30 characters',
                                  error_messages = { 'required': 'You must supply your last name.',
                                                     'max_length': 'A maximum of 30 characters, please.'},
                                  max_length=30)

    email_address = forms.EmailField( label = 'Email Address',
                                      initial = 'Enter your email address',
                                      widget = forms.TextInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                                      help_text = 'Your valid email address, up to 200 characters.',
                                      error_messages = { 'required': 'You must supply an email address.',
                                                         'invalid': 'That does not appear to be a valid email address.',
                                                         'max_length': 'A maximum of 200 characters, please.'},
                                      max_length=200)

    password = forms.CharField(label = 'Password',
                               initial = 'Enter a password',
                               widget = forms.PasswordInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                               help_text = 'Pick a strong password between 8 and 30 characters long.',
                               error_messages={'required': 'You must choose a password',
                                               'max_length':
                                               'That is an awfully long password!  A max of 30 characters, please!',
                                               'min_length':
                                               'Choose a longer password.  A minimum of 8 characters, please.'},
                               min_length=8,
                               max_length=30)

    password_verify = forms.CharField(label = 'Verify Password',
                                      initial = 'Verify your password',
                                      widget = forms.PasswordInput(attrs = {'rows' : 1, 'class' : 'span4 input-large'}),
                                      help_text = 'Re-enter your password.',
                                      error_messages={'required': 'You must enter your password twice.'},
                                      max_length=30)

    accepts_terms = forms.BooleanField(
                                       error_messages={'required': 'You must accept the Terms and Conditions'})

    def clean_password(self):
        '''
        Verifies that the password matches the user-provided verfication and ensures it has appropriate
        complexity.
        '''
        candidate = self.data['password']
        if candidate != self.data['password_verify']:
            raise forms.ValidationError('Your passwords don\'t match.  Please try again.')

        # TODO: need complexity calculation here
        return self.data['password']



