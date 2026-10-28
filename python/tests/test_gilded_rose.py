# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_invalid_numeric_types_are_rejected_before_any_item_is_updated(self):
        for field in ["sell_in", "quality"]:
            for value in [1.5, 1.0, "1", None, True, False]:
                with self.subTest(field=field, value=value):
                    valid = Item("Aged Brie", 2, 10)
                    invalid = Item("Conjured Mana Cake", 2, 10)
                    setattr(invalid, field, value)
                    before = [vars(item).copy() for item in [valid, invalid]]

                    with self.assertRaises(TypeError) as error:
                        GildedRose([valid, invalid]).update_quality()

                    self.assertIn(invalid.name, str(error.exception))
                    self.assertIn(field, str(error.exception))
                    self.assertIn(repr(value), str(error.exception))
                    self.assertIn("integer", str(error.exception))
                    self.assertEqual(before, [vars(valid), vars(invalid)])

    def test_invalid_quality_is_rejected_before_any_item_is_updated(self):
        names = ["ordinary", "Aged Brie", "Backstage passes to a TAFKAL80ETC concert", "Conjured Mana Cake"]
        cases = [(name, quality) for name in names for quality in [-1, 51]]
        cases += [("Sulfuras, Hand of Ragnaros", quality) for quality in [0, 50, 79, 81]]
        for name, quality in cases:
            with self.subTest(name=name, quality=quality):
                valid = Item("Aged Brie", 2, 10)
                invalid = Item(name, -1, quality)
                before = [vars(item).copy() for item in [valid, invalid]]

                with self.assertRaises(ValueError) as error:
                    GildedRose([valid, invalid]).update_quality()

                self.assertIn(name, str(error.exception))
                self.assertIn("quality", str(error.exception))
                self.assertIn(str(quality), str(error.exception))
                self.assertIn("80" if name.startswith("Sulfuras") else "0..50", str(error.exception))
                self.assertEqual(before, [vars(valid), vars(invalid)])

    def test_conjured_items_lose_two_quality_before_sell_by_date(self):
        for name in ["Conjured Mana Cake", "Conjured Elixir"]:
            with self.subTest(name=name):
                self.assert_daily_update(name, 1, 10, 8)

    def test_conjured_items_lose_four_quality_at_and_after_sell_by_date(self):
        for sell_in in [0, -1]:
            with self.subTest(sell_in=sell_in):
                self.assert_daily_update("Conjured Mana Cake", sell_in, 10, 6)

    def test_conjured_quality_stops_at_zero(self):
        cases = [(1, 0), (1, 1), (1, 2), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (-1, 3)]
        for sell_in, quality in cases:
            with self.subTest(sell_in=sell_in, quality=quality):
                self.assert_daily_update("Conjured Mana Cake", sell_in, quality, 0)

    def test_conjured_item_crosses_sell_by_date_over_multiple_days(self):
        item = Item("Conjured Mana Cake", 1, 9)
        shop = GildedRose([item])
        for expected in [(0, 7), (-1, 3), (-2, 0), (-3, 0)]:
            with self.subTest(expected=expected):
                shop.update_quality()
                self.assertEqual(expected, (item.sell_in, item.quality))

    def test_conjured_prefix_is_case_sensitive_and_requires_a_space(self):
        for name in ["conjured Mana Cake", "ConjuredMana Cake", "Elixir Conjured", "Conjured"]:
            with self.subTest(name=name):
                self.assert_daily_update(name, 1, 10, 9)

    def assert_daily_update(self, name, sell_in, quality, expected_quality):
        item = Item(name, sell_in, quality)

        GildedRose([item]).update_quality()

        self.assertEqual(expected_quality, item.quality)
        self.assertEqual(sell_in - 1, item.sell_in)
        self.assertEqual(name, item.name)

    def test_normal_items_lose_quality_twice_as_fast_after_sell_by_date(self):
        for sell_in, expected_quality in [(1, 9), (0, 8), (-1, 8)]:
            with self.subTest(sell_in=sell_in):
                self.assert_daily_update("Elixir of the Mongoose", sell_in, 10, expected_quality)


    def test_normal_item_quality_never_becomes_negative(self):
        for sell_in in [1, 0, -1]:
            for quality in [0, 1]:
                with self.subTest(sell_in=sell_in, quality=quality):
                    self.assert_daily_update("+5 Dexterity Vest", sell_in, quality, 0)

    #2 days quality increase present in the code, but not in the requirements
    def test_aged_brie_gains_quality_twice_as_fast_after_sell_by_date(self):
        for sell_in, expected_quality in [(1, 11), (0, 12), (-1, 12)]:
            with self.subTest(sell_in=sell_in):
                self.assert_daily_update("Aged Brie", sell_in, 10, expected_quality)

    def test_aged_brie_quality_never_exceeds_fifty(self):
        for sell_in in [1, 0, -1]:
            for quality in [49, 50]:
                with self.subTest(sell_in=sell_in, quality=quality):
                    self.assert_daily_update("Aged Brie", sell_in, quality, 50)

    def test_backstage_passes_gain_quality_as_concert_approaches(self):
        cases = [(11, 21), (10, 22), (6, 22), (5, 23), (1, 23)]
        for sell_in, expected_quality in cases:
            with self.subTest(sell_in=sell_in):
                self.assert_daily_update(
                    "Backstage passes to a TAFKAL80ETC concert", sell_in, 20, expected_quality
                )

    def test_backstage_pass_quality_never_exceeds_fifty(self):
        cases = [
            (11, 49, 50), (11, 50, 50),
            (10, 48, 50), (10, 49, 50), (10, 50, 50),
            (5, 48, 50), (5, 49, 50), (5, 50, 50),
        ]
        for sell_in, quality, expected_quality in cases:
            with self.subTest(sell_in=sell_in, quality=quality):
                self.assert_daily_update(
                    "Backstage passes to a TAFKAL80ETC concert",
                    sell_in,
                    quality,
                    expected_quality,
                )

    def test_backstage_passes_are_worthless_after_concert(self):
        for sell_in in [0, -1]:
            for quality in [0, 20, 50]:
                with self.subTest(sell_in=sell_in, quality=quality):
                    self.assert_daily_update(
                        "Backstage passes to a TAFKAL80ETC concert", sell_in, quality, 0
                    )

    def test_sulfuras_never_changes(self):
        for sell_in in [1, 0, -1]:
            with self.subTest(sell_in=sell_in):
                item = Item("Sulfuras, Hand of Ragnaros", sell_in, 80)

                GildedRose([item]).update_quality()

                self.assertEqual(80, item.quality)
                self.assertEqual(sell_in, item.sell_in)
                self.assertEqual("Sulfuras, Hand of Ragnaros", item.name)

    def test_empty_inventory_can_be_updated(self):
        items = []

        GildedRose(items).update_quality()

        self.assertEqual([], items)

    def test_mixed_inventory_updates_original_items_in_place(self):
        normal = Item("Elixir of the Mongoose", 1, 10)
        brie = Item("Aged Brie", 0, 10)
        sulfuras = Item("Sulfuras, Hand of Ragnaros", 0, 80)
        passes = Item("Backstage passes to a TAFKAL80ETC concert", 5, 10)
        items = [normal, brie, sulfuras, passes]
        shop = GildedRose(items)

        shop.update_quality()

        self.assertIs(items, shop.items)
        self.assertEqual(4, len(items))
        for actual, original, expected in zip(
            items,
            [normal, brie, sulfuras, passes],
            [(0, 9), (-1, 12), (0, 80), (4, 13)],
        ):
            with self.subTest(name=original.name):
                self.assertIs(original, actual)
                self.assertEqual(expected, (actual.sell_in, actual.quality))

    def test_normal_item_crosses_sell_by_date_over_multiple_days(self):
        item = Item("Elixir of the Mongoose", 1, 4)
        shop = GildedRose([item])

        for expected in [(0, 3), (-1, 1), (-2, 0), (-3, 0)]:
            with self.subTest(expected=expected):
                shop.update_quality()
                self.assertEqual(expected, (item.sell_in, item.quality))


if __name__ == '__main__':
    unittest.main()
