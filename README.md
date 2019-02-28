# utddirectory

Python module to search the UTD Directory using python.

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
