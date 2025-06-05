## Использование модуля

### 1. Установка и настройка

1. Поместите модуль в папку addons Odoo
2. Обновите список модулей: `Настройки -> Модули -> Обновить список модулей`
3. Установите модуль `yandex_geo_widget`
4. Получите API ключ Yandex Maps и добавьте в системные параметры:
   (это необходимо если вы хотите работать не только с координатами, но и с адресами,
   для работы с координатами ключ не обязателен)
   - Api ключ можно получить тут https://developer.tech.yandex.ru
   - Перейдите в `Настройки -> Технические -> Параметры -> Системные параметры`
   - Создайте параметр с ключом `yandex_geo_widget.api_key` и значением вашего API ключа

### 2. Подключение к существующей модели

```python
# В вашей модели добавьте наследование от mixin
class YourModel(models.Model):
    _name = 'your.model'
    _inherit = ['your.model', 'geo.mixin']

    # Ваши поля...
```

```xml
<!-- В XML представлении добавьте поле с виджетом -->
<field name="address_text" widget="geo_yandex_map"/>
```

### 3. Создание новой модели с адресом

```python
class DeliveryPoint(models.Model):
    _name = 'delivery.point'
    _inherit = ['geo.mixin']
    _description = 'Точка доставки'

    name = fields.Char('Название', required=True)
    # geo_address, geo_latitude, geo_longitude уже доступны из mixin
```
