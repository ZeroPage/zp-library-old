from django import forms

class BookForm(forms.Form):
    ISBN = forms.CharField()
    title = forms.CharField()
    author = forms.CharField()
    translator = forms.CharField()
    publisher = forms.CharField()
    publishedDate = forms.DateField()
    description = forms.CharField(widget=forms.Textarea)
    category = forms.CharField()
    language = forms.CharField()
    smallThumbnail = forms.CharField()
    thumbnail = forms.CharField()
    pageCount = forms.IntegerField()
    bookCount = forms.IntegerField()
    donor = forms.CharField()

    def action(self):
        # send email using the self.cleaned_data dictionary
        pass