import unittest
from domain.entities import KpopGroup

class TestKpopGroup(unittest.TestCase):

    def test_create_group(self):
        group = KpopGroup("BTS", 7)
        self.assertEqual(group.name, "BTS")
        self.assertEqual(group.members, 7)

    def test_change_name(self):
        group = KpopGroup("EXO", 9)
        group.name = "EXO-L"
        self.assertEqual(group.name, "EXO-L")

    def test_change_members(self):
        group = KpopGroup("TWICE", 9)
        group.members = 10
        self.assertEqual(group.members, 10)

if __name__ == "__main__":
    unittest.main()
