from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
from .color import Color


class ColorDict(Data):
    """Class representing a dictionary of colors.

    Parameters
    ----------
    default : :class:`compas.colors.Color`
        The default color to use if the requested key is not in the dictionary.

    Attributes
    ----------
    default : :class:`compas.colors.Color`
        The default color to use if the requested key is not in the dictionary.

    """

    def __init__(self, default, **kwargs):
        super(ColorDict, self).__init__(**kwargs)
        self._default = None
        self.default = default
        self._dict = {}

    @property
    def default(self):
        if not self._default:
            self._default = Color(0, 0, 0)
        return self._default

    @default.setter
    def default(self, default):
        if default and not isinstance(default, Color):
            default = Color.coerce(default)
        self._default = default

    def __getitem__(self, key):
        return self._dict.get(key, self.default)

    def __setitem__(self, key, value):
        self._dict[key] = Color.coerce(value)

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return key in self._dict

    @property
    def data(self):
        return {"default": self.default.data, "dict": self._dict}

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def get(self, key, default=None):
        return self._dict.get(key, default or self.default)

    def clear(self):
        """Clear the previously stored items.

        Returns
        -------
        None

        """
        self._dict = {}

    def update(self, other):
        """Update the dictionary with the items from another dictionary.

        Parameters
        ----------
        other : dict or :class:`compas.scene.ColorDict`
            The other dictionary.

        Returns
        -------
        None

        """
        for key, value in other.items():
            self[key] = value
