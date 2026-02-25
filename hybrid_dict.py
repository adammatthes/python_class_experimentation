class HybridDict():
    def fromkeys(iterable, value=None):
        return HybridDict(dict.fromkeys(iterable, value))

    def __init__(self, data=None):
        if data is not None and not isinstance(data, dict):
            raise ValueError("HybridDict only takes a dictionary as an optional argument")
        self._data = {} if data is None else data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'HybridDict' object has no attribute '{name}'")

    def __delitem__(self, key):
        try:
            del self._data[key]
        except KeyError:
            raise AttributeError(f"'HybridDict' object has no attribute '{key}'")

    def __eq__(self, other):
        if isinstance(other, HybridDict):
            return self._data == other._data
        elif isinstance(other, dict):
            return self._data == other

        raise TypeError(f"Comparison not supported between HybridDict and {other.__class__}")


    def __setattr__(self, name, value):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def __or__(self, other):
        if isinstance(other, HybridDict):
            self._data = self._data | other._data
            return self
        elif isinstance(other, dict):
            self._data |= other
            return self
        
        raise TypeError(f"Operation not supported between HybridDict and {other.__class__}")

    def __ior__(self, other):
        if isinstance(other, HybridDict):
            self._data = self._data | other._data
            return self
        elif isinstance(other, dict):
            self._data |= other
            return self

        raise TypeError(f"Operation not supported between HybridDict and {other.__class__}")

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return len(self._data)

    def __reversed__(self):
        return self._data.__reversed__()

    def get(self, attr, default=None):
        return self._data.get(attr, default)

    def clear(self):
        self._data.clear()

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def copy(self):
        return HybridDict(self._data)

    def pop(self, key, default=None):
        result = self._data.pop(key, default)
        return result

    def popitem(self):
        return self._data.popitem()

    def setdefault(self, key, default=None):
        self._data.setdefault(key, default)

    def update(self, E, F=None):
        self._data.update(E)
        if F is not None:
            self._data.update(F)

    def values(self):
        return self._data.values()


