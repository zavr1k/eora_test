# API бот которые помогает поределить кот перед вами или хлеб =)
[![Base Checks](https://github.com/zavr1k/eora_test/actions/workflows/checks.yml/badge.svg)](https://github.com/zavr1k/eora_test/actions/workflows/checks.yml)

### Принцип работы
* Для начала работы нужно создать пользователя. Отравьте post запрос на ендпоинт `/user`. 
  В ответ вы получете id пользователя, он будет необходим для дальнейшей работы с ботом.
* Для общения с ботом оправьте post запрос на `/send_message` со следующим содержимым:
  ```
  {
    'user_id': '1',
    'message' '/start'
  }
  ```
* Продолжайте отвечать на вопросы бота.
  
Подробное описание API доступно по ссылка `/docs` или `/redoc`
