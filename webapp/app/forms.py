from django import forms
from django.core.exceptions import ValidationError

import requests

from app.tools import user, login_url, save_user, load_user

css_class = "form-control border-0 shadow form-control-lg"


class CreateUserForm(forms.Form):
    first_name = forms.CharField(
        label="Prénom(s)",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    email = forms.EmailField(
        label="Adresse mail",
        max_length=30,
        widget=forms.EmailInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": css_class,
            },
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        password2 = cleaned_data["password2"]
        if password != password2:
            raise ValidationError(
                "Les mots de passe ne concordent pas.", code="password_mismatch"
            )
        return cleaned_data


class ConnectionForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "class": css_class,
            },
        ),
    )

    def clean(self):
        global user
        cleaned_data = super().clean()
        response = requests.post(login_url, json=cleaned_data)
        if response.status_code == requests.codes.ok:
            response = response.json()
            user["token"] = response["token"]
            user["is_auth"] = True
            user["username"] = cleaned_data["username"]
            user["email"] = response["email"]
            user["id"] = response["id"]
            save_user(user)
            user = load_user()
            return cleaned_data
        else:
            if "non_field_errors" in response.json():
                raise ValidationError(
                    response.json()["non_field_errors"], code="incorrect"
                )
            else:
                raise ValidationError("Erreur de connexion", code="incorrect")


class AddProductForm(forms.Form):
    designation = forms.CharField(
        label="Désignation",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    price = forms.FloatField(
        label="Prix (en Franc CFA)",
        widget=forms.NumberInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    stock = forms.FloatField(
        label="Stock",
        widget=forms.NumberInput(
            attrs={
                "class": css_class,
            },
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": css_class,
            },
        ),
    )
