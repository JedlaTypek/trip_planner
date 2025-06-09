from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Place, EntryFee, Trip


class PlaceForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        label="Nové štítky (oddělené čárkou)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Zadejte nové štítky, pokud chcete přidat jiné než ve výběru."
    )

    class Meta:
        model = Place
        fields = ['name', 'description', 'opening_hours', 'featured_image', 'google_maps_url', 'tags']
        labels = {
            'name': 'Název místa',
            'description': 'Popis místa',
            'opening_hours': 'Otevírací doba',
            'featured_image': 'Náhledový obrázek',
            'google_maps_url': 'Odkaz na google mapy',
            'tags': 'Štítky'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'opening_hours': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'google_maps_url': forms.URLInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }



class EntryFeeForm(forms.ModelForm):
    class Meta:
        model = EntryFee
        fields = ['category', 'price']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kategorie'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cena'}),
        }

EntryFeeFormSet = inlineformset_factory(
    Place,
    EntryFee,
    form=EntryFeeForm,
    extra=1,
    can_delete=True
)

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'date', 'places']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'places': forms.SelectMultiple(attrs={'size': 4, 'class': 'form-control'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Zadejte platný e-mail.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']