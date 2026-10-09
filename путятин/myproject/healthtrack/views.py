# healhtrack/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Measurement
from .forms import MeasurementForm
import json
from django.utils import timezone
from datetime import timedelta

@login_required
def overview(request):
    alert_context = None
    from .models import UserProfile  
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    
    # 1. ОБРАБОТКА ФОРМЫ (Сначала сохраняем данные в базу)
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            
            is_normal = (
                profile_obj.target_systolic_min <= measurement.systolic <= profile_obj.target_systolic_max and
                profile_obj.target_diastolic_min <= measurement.diastolic <= profile_obj.target_diastolic_max
            )
            
            if not is_normal:
                alert_context = {
                    'type': 'danger',
                    'title': 'Выше цели',
                    'message': 'Давление выше вашей цели. Это отдельное измерение, не диагноз. Спокойно отдохните 5 минут и измерьте давление ещё раз.',
                    'systolic': measurement.systolic,
                    'diastolic': measurement.diastolic,
                    'pulse': measurement.pulse
                }
            
            form = MeasurementForm()
    else:
        form = MeasurementForm()

    # 2. ПОЛУЧЕНИЕ ДАННЫХ (Перенесли сюда, теперь тут всегда актуальная база!)
    week_ago = timezone.now() - timedelta(days=7)
    
    # Для графиков нам нужна сортировка от старых к новым (.order_by('timestamp'))
    measurements = Measurement.objects.filter(user=request.user, timestamp__gte=week_ago).order_by('timestamp')
    
    # ИСПРАВЛЕНО: Чтобы взять САМОЕ ПОСЛЕДНЕЕ измерение, берем элемент с конца списка (.last())
    # Если список отсортирован по возрастанию времени, то .last() — это самый свежий замер
    last_measurement = measurements.last() if measurements.exists() else None

    # Подготовка данных для Chart.js
    labels = [m.timestamp.strftime('%d.%m') for m in measurements]
    systolic_data = [m.systolic for m in measurements]
    diastolic_data = [m.diastolic for m in measurements]

    chart_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Верхнее (систолическое)',
                'data': systolic_data,
                'borderColor': '#1976d2',
                'backgroundColor': 'rgba(25, 118, 210, 0.1)',
                'tension': 0.3,
            },
            {
                'label': 'Нижнее (диастолическое)',
                'data': diastolic_data,
                'borderColor': '#4fc3f7',
                'backgroundColor': 'rgba(79, 195, 247, 0.1)',
                'tension': 0.3,
            }
        ]
    }

    context = {
        'form': form,
        'measurements': measurements,
        'chart_data': json.dumps(chart_data), 
        'alert_context': alert_context,
        'profile': profile_obj,  
        'last_measurement': last_measurement, # Передаем актуальный замер
    }
    
    return render(request, 'healthtrack/overview.html', context)