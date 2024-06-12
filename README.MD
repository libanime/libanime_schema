# libanime codegen
Эта библиотека содержит конфигурации для генерации структур-вебпарсеров на основе [selector-schema-codegen](https://github.com/vypivshiy/selector_schema_codegen) 

src - конфигурации парсеров для источников
player - конфигурации парсеров для плееров

## Usage

```
ssc_gen CONFIGS.py | FOLDER... -c [dialect] -o [output_path]
```
### Example

```shell
# python
# generate code usage bs4 lib
ssc_gen src/animego.py -c py.bs4
# generate code usage parsel lib
ssc_gen src/animego.py -c py.parsel

# dart code generator
ssc_gen src/animego.py -c dart
# generate all configs from folder
ssc_gen src -c dart
```

## Модификация, быстрые исправления

Рекомендуется использовать наследование с перезаписью методов.
Методы для полей обычно имеют префикс `parse`

Пример:

```python
from animego import Ongoing

class PatchedOngoing(Ongoing):
    
    @staticmethod
    def _parse_dub(part) -> str:
        # patch dubber output example
        val_0 = part.select_one(".text-gray-dark-6").text
        return val_0.replace('(', '').replace(')', '').lower()
    
    # some any patches ...
```
