# LentaMobParser
* **Описание**: Парсинг товаров категории 'Животные' (более 100 штук) для городов Москва и Санкт-Петербург и выгрузка в формат csv. Все товары в наличии.
Парсер использует только те эндпоинты, которые использует мобильное приложение.
* **Установка**  
Клонировать репозиторий:

```
git clone git@github.com:KatyaSoloveva/LentaMobParser.git
```  

Создать и активировать виртуальное окружение:
```
python -m venv venv
```

Для Windows
```
venv/Scripts/activate
```

Для Linux
```
source venv/bin/activate
```
Выполнить:
```
pip install -r requirements.txt
```

Запустить:
```
python main.py
```