from __future__ import annotations


class AbstractMenuLayer:
    _elements = None

    def on_show(self):
        pass

    def on_select(self, element) -> AbstractMenuLayer:
        pass

    def get_elements(self):
        return self._elements
