## Использование модуля

### 1. Установка и настройка

1. Поместите модуль в папку addons Odoo
2. Обновите список модулей: `Настройки -> Модули -> Обновить список модулей`
3. Установите модуль `field_widget_fias`
4. Получите API ключ FIAS и добавьте в системные параметры:
   - Перейдите в `Настройки -> Технические -> Параметры -> Системные параметры`
   - Создайте параметр с ключом `field_widget_fias.api_key` и значением вашего API ключа

### 2. Подключение к полю модели

```xml
<!-- В XML представлении добавьте поле с виджетом -->
<field name="address_text" widget="field_widget_fias"/>
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
