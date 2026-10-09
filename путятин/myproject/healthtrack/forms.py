# healhtrack/forms.py

from django import forms
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
    # 1. УБРАЛИ 'timestamp' из этого списка
        fields = ['systolic', 'diastolic', 'pulse', 'note'] 
        
        widgets = {
            'systolic': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Например, 120',
                'min': 50,
                'max': 250
            }),
            'diastolic': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Например, 80',
                'min': 30,
                'max': 150
            }),
            'pulse': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Например, 75',
                'min': 30,
                'max': 200
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2, 
                'placeholder': 'Заметки (выпил кофе, стресс и т.д.)'
            }),
            # 2. УБРАЛИ виджет для 'timestamp' отсюда совсем
        }

    def clean(self):
        cleaned_data = super().clean()
        systolic = cleaned_data.get('systolic')
        diastolic = cleaned_data.get('diastolic')
        pulse = cleaned_data.get('pulse')

        if systolic and systolic > 250:
            self.add_error('systolic', 'Верхнее давление не может быть выше 250.')
        if diastolic and diastolic > 150:
            self.add_error('diastolic', 'Нижнее давление не может быть выше 150.')
        if pulse and pulse > 200:
            self.add_error('pulse', 'Пульс не может быть выше 200.')