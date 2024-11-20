import json
from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'tipo_curso', 'apresent', 'said_prof', 'planocur', 'avqual', 'outr_inf']

    def clean_avqual(self):
        data = self.cleaned_data.get('avqual')
        if isinstance(data, str):
            return [int(x) for x in data.split(',') if x.isdigit()]
        return data

    def clean_outr_inf(self):
        data = self.cleaned_data.get('outr_inf')
        if data:
            try:
                # Tenta converter a string JSON em um dicionário
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError("As informações devem estar em formato JSON válido.")
        return {}
