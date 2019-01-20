class NestedDict(dict):
    """

    A NestedDict is a dictionary in which nested objects can be accessed used
    a dotted key notation. It is a direct sub-class of `dict` and supports all the
    standard `dict` operations. However you can created nested dict entries by
    seperating the key string with dots '.'.

    Hence

    >>> a = NestedDict({"a":{"b":{"c":1}}})
    >>> a
    {'a': {'b': {'c': 1}}}
    >>> a['a.b.c']
    1
    >>> a['a.b.c']=2
    >>> a['a.b.c']
    2
    >>> a["a.b"]
    {'c': 1}

    Keys must be strings. Keys of other types will raise a KeyError exception.

    """

    def _key_split(self, key):
        """
        Split a key into its component parts

        >>> a = NestedDict()
        >>> a._key_split("a.b.c")
        ['a', 'b', 'c']
        >>> a._key_split(3)
        Traceback (most recent call last):
        ValueError: Expected a <str> type

        :param key: a key of the form "a.b.c.d"
        :return: ['a', 'b', 'c', 'd']
        """
        if isinstance(key, str):
            return key.split('.')
        else:
            raise ValueError("Expected a <str> type")

    def _has_nested(self, d, keys):
        """
        Does this dict have the list of keys specified in `keys`.
        Uses recursion to walk the list of keys. All keys must be present.
        :param d: a dict
        :param keys: a list of keys
        :return: bool
        """
        if len(keys) > 1 and isinstance(d, dict):
            if dict.__contains__(d, keys[0]):
                return self._has_nested(d[keys[0]], keys[1:])
            else:
                return False
        else:
            return dict.__contains__(d, keys[0])

    def _get_nested(self, d, keys):
        """
        For any given list of keys return the value of the nested
        set of dictionaries.
        :param d: a NestedDict
        :param keys: a list of key strings
        :return: a value
        >>> a=NestedDict()
        >>> a['a.b.c'] = 1
        >>> a._get_nested(a, ['a', 'b', 'c'])
        1
        >>> a._get_nested(a, ['a', 'b'])
        {'c': 1}
        """
        if len(keys) > 1 and isinstance(d, dict):
            if dict(d).__contains__(keys[0]):
                return self._get_nested(d[keys[0]], keys[1:])
            else:
                raise KeyError(f"no such key: {keys[0]}")
        else:
            return dict.__getitem__(d, keys[0])

    def _set_nested(self, d, keys, value):
        """
        Set the value of a NestedDict element creating the necessary
        dictionaries if they don't exist.
        :param d: A NestedDict
        :param keys: a list of key strings e.g ['a', 'b', 'c']
        :param value: a value to set
        :return: a NestedDict with `value` = d['a.b.c']

        >>> a=NestedDict()
        >>> a['a.b.c'] = 1
        >>> a
        {'a': {'b': {'c': 1}}}
        >>>
        >>> a['a.b']
        {'c': 1}

        """
        if len(keys) > 1 and isinstance(d, dict):
            if dict(d).__contains__(keys[0]) and isinstance(d[keys[0]], dict):
                return self._set_nested(d[keys[0]], keys[1:], value)
            else:
                d[keys[0]] = {}
                return self._set_nested(d[keys[0]], keys[1:], value)
        else:
            dict.__setitem__(d, keys[0], value)

    def _del_nested(self, d, keys):
        if len(keys) > 1 and isinstance(d, dict):
            if dict(d).__contains__(keys[0]):
                return self._del_nested(d[keys[0]], keys[1:])
            else:
                dict.__delitem__(d, keys[0])
        else:
            dict.__delitem__(d, keys[0])

    def _apply_init(self, seq, **kwargs):
        if seq is None:
            self={}
        elif isinstance(seq, dict):
            for k,v in seq.items():
                if isinstance(k, str):
                    self._set_nested(self,k.split('.'), v)
                else:
                    raise ValueError(f"{k} is not a string type")
        elif isinstance(seq, list)or isinstance(seq, set):
            for k,v in seq:
                if isinstance(k, str):
                    self._set_nested(self,k.split('.'), v)
                else:
                    raise ValueError(f"{k} is not a string type")
        else:
            raise ValueError(f"{seq} is not a dict, list, or set")

        for k, v in kwargs.items():
            if isinstance(k, str):
                self._set_nested(self, k.split('.'), v)
            else:
                raise ValueError(f"{k} is not a string type")

        return self

    def __init__(self, seq=None, **kwargs):  # known special case of dict.__init__
        """
        Allows all the various methods of initialising dictionaries but
        will throw a KeyError is the keys are not strings.

        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        # (copied from class doc)
        """

        self._apply_init(seq, **kwargs)

    def __contains__(self, key):
        """`key in self` where is key is a str and may be dotted e.g. 'a.b.c'"""

        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        return self._has_nested(self, key.split('.'))

    def __getitem__(self, key):
        """Return item indexed by key"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        return self._get_nested(self, key.split('.'))

    def __setitem__(self, key, value):
        """Set key to value where key can be dotted notation e.g. 'a.b.c'"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        self._set_nested(self, key.split('.'), value)

    def get(self, key, default_value=None):
        """Return key or if key not present return `default_value`"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        try:
            return self._get_nested(self, key.split('.'))
        except KeyError:
            return default_value

    def has_key(self, key):
        """key in self"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        try:
            return self._get_nested(self, key.split('.'))
        except KeyError:
            return False

    def __delitem__(self, key):
        """Remove key from collection"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        self._del_nested(self, key.split('.'))

    def pop(self, key, default_value=None):
        """Remove key and return value associated with key. if key not present
        return `default_value`"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        try:
            v = self._get_nested(self, key.split('.'))
            self._del_nested(self, key.split('.'))
        except KeyError:
            v = default_value

        return v

    def popitem(self, key):
        """Return the last item added to the dict and remove the item"""
        if not isinstance(key, str):
            raise ValueError(f"{key} is not a string type")
        v = self._get_nested(self, key.split('.'))
        self._del_nested(self, key.split('.'))
        return key, v

    def update(self, E=None, **F):  # known special case of dict.update
        """
        `D.update([E, ]**F) -> None`.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  `for k in E: D[k] = E[k]`
        If E is present and lacks a .keys() method, then does:  `for k, v in E: D[k] = v`
        In either case, this is followed by: `for k in F:  D[k] = F[k]`

        In all cases non `str` keys will throw a KeyError exception.
        """
        return self._apply_init(E, **F)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
