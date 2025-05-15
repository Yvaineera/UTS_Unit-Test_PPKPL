import unittest
from domain.entities import KpopGroup
from data.group_repository import GroupRepository

class TestGroupRepository(unittest.TestCase):

    def setUp(self):
        self.repo = GroupRepository()

    def test_add_new_group_success(self):
        group = KpopGroup("BTS", 7)
        result = self.repo.add(group)
        self.assertTrue(result)

    def test_add_duplicate_group(self):
        group = KpopGroup("BTS", 7)
        self.repo.add(group)
        result = self.repo.add(group)
        self.assertFalse(result)

    def test_add_multiple_groups(self):
        g1 = KpopGroup("BTS", 7)
        g2 = KpopGroup("EXO", 9)
        self.assertTrue(self.repo.add(g1))
        self.assertTrue(self.repo.add(g2))

    def test_browse_all_groups(self):
        self.repo.add(KpopGroup("BLACKPINK", 4))
        self.repo.add(KpopGroup("TWICE", 9))
        groups = self.repo.browse()
        self.assertEqual(len(groups), 2)

    def test_browse_empty_repository(self):
        groups = self.repo.browse()
        self.assertEqual(groups, [])

    def test_browse_after_deletion(self):
        self.repo.add(KpopGroup("EXO", 9))
        self.repo.delete("EXO")
        self.assertEqual(self.repo.browse(), [])

    def test_read_existing_group(self):
        self.repo.add(KpopGroup("AESPA", 4))
        group = self.repo.read("AESPA")
        self.assertIsNotNone(group)
        self.assertEqual(group.name, "AESPA")

    def test_read_nonexistent_group(self):
        result = self.repo.read("IVE")
        self.assertIsNone(result)

    def test_read_after_add_and_delete(self):
        self.repo.add(KpopGroup("NMIXX", 7))
        self.repo.delete("NMIXX")
        result = self.repo.read("NMIXX")
        self.assertIsNone(result)

    def test_edit_existing_group(self):
        self.repo.add(KpopGroup("LE SSERAFIM", 5))
        result = self.repo.edit("LE SSERAFIM", new_members=6)
        self.assertTrue(result)
        updated = self.repo.read("LE SSERAFIM")
        self.assertEqual(updated.members, 6)

    def test_edit_nonexistent_group(self):
        result = self.repo.edit("OMG", KpopGroup("OMG", 5))
        self.assertFalse(result)

    def test_edit_name_change(self):
        self.repo.add(KpopGroup("LOONA", 12))
        result = self.repo.edit("LOONA", new_name="LOONA1", new_members=13)
        self.assertTrue(result)
        self.assertIsNotNone(self.repo.read("LOONA1"))
        self.assertEqual(self.repo.read("LOONA1").members, 13)

    def test_delete_existing_group(self):
        self.repo.add(KpopGroup("SNSD", 8))
        result = self.repo.delete("SNSD")
        self.assertTrue(result)
        self.assertIsNone(self.repo.read("SNSD"))

    def test_delete_nonexistent_group(self):
        result = self.repo.delete("SHINee")
        self.assertFalse(result)

    def test_delete_then_add_same_group(self):
        self.repo.add(KpopGroup("SEVENTEEN", 13))
        self.repo.delete("SEVENTEEN")
        result = self.repo.add(KpopGroup("SEVENTEEN", 13))
        self.assertTrue(result)
