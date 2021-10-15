import unittest


from wtoolzargs.common import mapping


class TestCommonMapping(unittest.TestCase):
    def test_mapping_create_from_strings(self):
        def upper(s):
            return s.upper()

        m = mapping.Mapping.create_from_strings("a.c", "b.d")
        self.assertListEqual(m.mappings(), [("a", "b"), ("c", "d")])

        m = mapping.Mapping.create_from_strings("a.c", ("b.d", upper))
        self.assertListEqual(m.mappings(), [("a", "b"), ("c", "d")])

    def test_mappings_create_from_dict(self):
        ms = mapping.Mappings.create_from_dict({"a": "b", "c.d": "e.f"})
        self.assertListEqual(ms.mappings().get("a"), [("a", "b")])
        self.assertListEqual(ms.mappings().get("c"), [("c", "e"), ("d", "f")])


if __name__ == "__main__":
    unittest.main(module="test_common_mapping")
