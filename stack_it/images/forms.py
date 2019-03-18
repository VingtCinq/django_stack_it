import imghdr

from django import forms

from stack_it.models import Image


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['folder', 'image', 'alt']
