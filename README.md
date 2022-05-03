# Приложение для управления персональными и рабочими заданиями


## Запуск приложения

1. Склонируйте репозиторий 

>git clone https://github.com/ipotemkin/todolist.git

2. Дальше есть две опции: запуск с фронтом и без него

2.1 С фронтом:

>docker-compose --file docker-test up -d

После запуска приложение доступно оп адресу: ```localhost:8080```

2.2 Без фронта – удобно, чтобы протестировать через swagger:

>docker-compose --file docker-test-back.yml up -d

После запуска приложение доступно по адресу: ```localhost:8000/``` или ```localhost:8000/swagger/```

## История разработки по домашкам
### Шаг первый (ДЗ 33):

- Создана кастомная модель пользователя
- Подключена админка Django
- Подключена база Postgres

### Шаг второй (ДЗ 34):

- Подключена ВМ
- Настроен автоматический деплой

### Шаг третий (ДЗ 35):

- Настроена авторизация пользователя по логину и паролю
- Настроена авторизация пользователя через VK
- Добавлен функционал просмотра и изменения профиля пользователя, в том числе, смена пароля


### Шаг четвертый (ДЗ 36):

- Добавлен функционал работы с категориями, целями и комментариями


### Шаг пятый (ДЗ 37):

- Добавлен функционал работы досками и их шеринг между пользователями
