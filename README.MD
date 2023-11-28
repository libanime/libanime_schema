# libanime codegen
This library contains configurations for generating parser schemes for unofficial API sources using
YAML + DSL-language [ssc_gen](https://github.com/vypivshiy/selector_schema_codegen) 

> These schemas just provide extractor logic

## languages support
| language | libraries      | xpath support | css support | formatter dependency |
|----------|----------------|---------------|-------------|----------------------|
| python   | bs4            | NO            | YES         | black                |
| python   | parsel         | YES           | YES         | black                |
| dart     | universal_html | NO            | YES         | dart format          |

## install

requirement python 3.10+

```shell
pip install ssc_gen
```

## usage
```
ssc_gen <scema_name>.yaml <language> -o <output>
```
### example

```shell
# python
# generate code usage bs4 lib
ssc_gen animego.yaml python.bs4 -o animego.py
# generate code usage parsel lib
ssc_gen animego.yaml python.parsel -o animego.py
# dart code generator
ssc_gen animego.yaml dart -o animego.dart
```

### generated classes usage

```dart
import 'animego.dart';
import 'package:dio/dio.dart';

void main() async {
  Map<String, String> headers = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
  };
  final client = Dio(BaseOptions(
      headers: headers
  ));
  var resp = await client.get("https://animego.org");
  // returns map structure
  var ongs = Ongoing(resp.toString()).parse().view();
  for (var i in ongs){
    print(i);
  }
}
```

```python
from animego import Ongoing
import requests

def main():
    response = requests.get("https://animego.org", headers={
        "User-Agent":
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    })
    ongs = Ongoing(response.text).parse().view()
    print(*ongs, sep='\n')


main()
```

## Modification, quick patches

Recommended to inherit from the generated class to prevent changes from being lost:

The value for the key is prefixed with `_parse` (`_parse_key`, `_parseKey`)

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
