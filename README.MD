# libanime codegen
This library contains configurations for generating parser schemes for unofficial API sources using
python + DSL-language [ssc_gen](https://github.com/vypivshiy/selector_schema_codegen) 

## Usage
```
ssc_gen <schema_name>.py <language> -o <output>
```
### Example

```shell
# python
# generate code usage bs4 lib
ssc_gen animego.py py.bs4 -o animego.py
# generate code usage parsel lib
ssc_gen animego.py py.parsel -o animego.py
# dart code generator
ssc_gen animego.py dart -o animego.dart
```

## Generated classes usage

pseudo-code
```
document = client.get(URL)
cls = SomeSchema(document).parse() // parse document
cls.view() // extract values
```

## Modification, quick patches

Recommended to inherit from the generated class to prevent changes from being lost:

The value for the key is prefixed with `_parse` (eg: `_parse_key`, `_parseKey`)

```python
from animego import Ongoing

class PatchedOngoing(Ongoing):
    
    @staticmethod
    def _parse_dub(part: BeautifulSoup) -> str:
        # patch dubber output example
        val_0 = part.select_one(".text-gray-dark-6").text
        return val_0.replace('(', '').replace(')', '').lower()
    
    # some any patches ...
```
