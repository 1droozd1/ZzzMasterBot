import datetime

def calculate_bedtime(wake_up_time):
    # Получаем текущую дату и время
    current_time = datetime.datetime.now()
    
    # Преобразуем введенное время для пробуждения в объект времени
    wake_up_hour, wake_up_minute = map(int, wake_up_time.split(':'))
    wake_up = current_time.replace(hour=wake_up_hour, minute=wake_up_minute, second=0, microsecond=0)
    
    # Если введенное время для пробуждения уже прошло сегодня, добавляем 1 день
    if wake_up < current_time:
        wake_up += datetime.timedelta(days=1)
    
    # Вычисляем оптимальное время для засыпания, вычитая среднюю продолжительность сна (в часах)
    average_sleep_duration = 8
    bedtime = wake_up - datetime.timedelta(hours=average_sleep_duration)

    while bedtime < current_time:
        bedtime += datetime.timedelta(hours=1, minutes=30)
    
    return bedtime.strftime("%H:%M")

# Пример использования функции
wake_up_time = input("Введите время для пробуждения (в формате ЧЧ:ММ): ")
bedtime = calculate_bedtime(wake_up_time)
print("Оптимальное время для засыпания:", bedtime)