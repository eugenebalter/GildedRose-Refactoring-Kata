# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self._validate_item(item)

        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue

            if item.name == "Aged Brie":
                self._increase_quality(item)
                if item.sell_in <= 0:
                    self._increase_quality(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self._increase_quality(item)
                if item.sell_in <= 10:
                    self._increase_quality(item)
                if item.sell_in <= 5:
                    self._increase_quality(item)
                if item.sell_in <= 0:
                    item.quality = 0
            else:
                degradation = 2 if item.name.startswith("Conjured ") else 1
                if item.sell_in <= 0:
                    degradation *= 2
                for _ in range(degradation):
                    self._decrease_quality(item)

            item.sell_in -= 1

    @staticmethod
    def _validate_item(item):
        for field in ("sell_in", "quality"):
            value = getattr(item, field)
            if type(value) is not int:
                raise TypeError(f"{item.name!r}: {field} must be an integer, got {value!r}")
        if item.name == "Sulfuras, Hand of Ragnaros":
            if item.quality != 80:
                raise ValueError(f"{item.name!r}: quality must be 80, got {item.quality}")
        elif not 0 <= item.quality <= 50:
            raise ValueError(f"{item.name!r}: quality must be in 0..50, got {item.quality}")

    @staticmethod
    def _increase_quality(item):
        if item.quality < 50:
            item.quality += 1

    @staticmethod
    def _decrease_quality(item):
        if item.quality > 0:
            item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
