# nesteddict

`class collections.NestedDict(self, seq=None, **kwargs)`

Return an instance of a dict subclass, supporting the usual dict
methods. An NestedDict is a dict that that only supports keys of type
`str`. Those keys may be nested by separating them with dots '.'. Hence a 
valid uses of `NestedDict` are:
```python
>>> from nesteddict import NestedDict
>>> a=NestedDict()
>>> a['x.y.z']=1
>>> a
{'x': {'y': {'z': 1}}}
>>> a['x.y']
{'z': 1}

```

Non `str` keys will throw a `KeyError` exception.


