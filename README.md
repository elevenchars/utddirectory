# utddirectory

Python module to search the UTD Directory using python.

## Installation
This has been tested on python 3.7.2.

```
pip install -r requirements.txt
```

## Command Line Usage
```
> python search.py [email/name/number] [emailhere]
Name: ...
Email: ...
Classification: ...
Major: ...
School: ...
```

## Module Usage
```python
from utddirectory import search
search.search(search.SearchType.NAME, "queryhere")
# returns name, email, classification, major, school in a dictionary. None if not found.
```
Search types are SearchType.NAME, SearchType.EMAIL, and SearchType.PHONE_NUMBER.

## Features
Search UTD directory by email, name, and number.

## Caveats
Currently only works if the search query is EXACT (there is only one result for the query).
