# utddirectory

Python module to search the UTD Directory using python.

## Installation
This has been tested on python 3.7.2.

```
pip install -r requirements.txt
```

## Command Line Usage
```
> python search.py email [emailhere]
Name: ...
Classification: ...
Major: ...
School: ...
```

## Module Usage
```python
from utddirectory import search
search.find_by_email("emailhere")
# returns name, classification, major, school in a dictionary
```

## Features
Search users by email.

## Planned Features
- Gracefully handle incorrect emails: possibly fill dict with None?
- Allow other search methods
- Consistent return for all methods
