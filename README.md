aftership-python
================

Basic example:
```python
import aftership

api = aftership.API('AFTERSHIP_API_KEY')
response = api.trackings.get(limit=10, page=2)
```