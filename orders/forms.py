from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order  # Правильное место для определения модели
        fields = ['user', 'first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Извлекаем request
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email

    def save(self, commit=True):  # Сохранение данных
        order = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            order.user = self.request.user
        if commit:
            order.save()
            return order