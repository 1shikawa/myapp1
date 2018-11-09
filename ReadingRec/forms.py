from django import forms
from .models import Book,Impression


class BookCreateForm(forms.ModelForm):
    """書籍のフォーム"""
    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Book
        fields = ('bookType', 'name', 'publisher', 'page', )


class ImpressionCreateForm(forms.ModelForm):
    """感想のフォーム"""
    def __init__(self, *args, **kwargs):
        super(ImpressionCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Impression
        fields = ('comment','readCount',)


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='※拡張子csvのファイルをアップロードしてください。')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.name.endswith('.csv'):
            return file
        else:
            raise forms.ValidationError('拡張子がcsvのファイルをアップロードしてください')


BookFormSet = forms.modelformset_factory(
    Book, form=BookCreateForm, extra=3, can_delete=True)

# BookFormSet = FormSet(queryset=Book.objects.none())