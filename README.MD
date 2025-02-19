# libanime codegen

Конфигурации для генерации структур-вебпарсеров при помощи [selector-schema-codegen](https://github.com/vypivshiy/selector_schema_codegen) 

- src - конфигурации парсеров для источников
- player - конфигурации парсеров для плееров

## Usage

```
ssc_gen <language> ...FILES/FOLDER -i [parser lib backend] -o [output_path]
```
### Examples

```shell
# python (bs4)
ssc_gen py src -i bs4 -o output
# python (parsel)
ssc_gen py src -i parsel -o output
# dart (universal_html)
ssc_gen dart src -o output
# golang (goquery)
ssc_gen go src -o output
# js (ES6, pure)
ssc_gen js src -o output
```

## Модификации и исправления

При повторной генерации кода все изменения будут потеряны, по возможности изменяйте файл конфигурации.
Если язык ООП - используйте наследование с переопределением методов или "патчи"
