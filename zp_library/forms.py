from django import forms

class BookForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def action(self):
        # send email using the self.cleaned_data dictionary
        pass