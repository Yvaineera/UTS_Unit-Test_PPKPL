import unittest
from domain.entities import KpopGroup
from usecases.group_service import GroupService
from data.group_repository import GroupRepository

class TestGroupService(unittest.TestCase):
    def setUp(self):
        self.repo = GroupRepository()
        self.service = GroupService(self.repo)

    def test_browse_with_data(self):
        self.service.add("BTS", 7)
        self.service.add("EXO", 9)
        result = self.service.browse()
        self.assertEqual(len(result), 2)

    def test_browse_empty(self):
        result = self.service.browse()
        self.assertEqual(len(result), 0)

    def test_browse_after_delete(self):
        self.service.add("BTS", 7)
        self.service.delete("BTS")
        result = self.service.browse()
        self.assertEqual(len(result), 0)

    def test_read_existing_group(self):
        self.service.add("EXO", 9)
        group = self.service.read("EXO")
        self.assertIsNotNone(group)
        self.assertEqual(group.name, "EXO")

    def test_read_nonexistent_group(self):
        group = self.service.read("TWICE")
        self.assertIsNone(group)

    def test_read_case_insensitive(self):
        self.service.add("Blackpink", 4)
        group = self.service.read("blackpink")
        self.assertIsNotNone(group)
        self.assertEqual(group.name, "Blackpink")

    def test_add_new_group(self):
        result = self.service.add("NewJeans", 5)
        self.assertTrue(result)

    def test_add_duplicate_group(self):
        self.service.add("NewJeans", 5)
        result = self.service.add("NewJeans", 5)
        self.assertFalse(result)

    def test_add_different_name_same_members(self):
        self.service.add("BTS", 7)
        result = self.service.add("StrayKids", 7)
        self.assertTrue(result)

    def test_edit_name_and_members(self):
        self.service.add("EXO", 9)
        result = self.service.edit("EXO", new_name="EXO-CBX", new_members=3)
        self.assertTrue(result)
        updated = self.service.read("EXO-CBX")
        self.assertEqual(updated.members, 3)

    def test_edit_to_existing_name(self):
        self.service.add("BTS", 7)
        self.service.add("EXO", 9)
        result = self.service.edit("EXO", new_name="BTS")
        self.assertFalse(result)

    def test_edit_members_only(self):
        self.service.add("Blackpink", 4)
        self.service.edit("Blackpink", new_members=5)
        updated = self.service.read("Blackpink")
        self.assertEqual(updated.members, 5)

    def test_delete_existing_group(self):
        self.service.add("EXO", 9)
        result = self.service.delete("EXO")
        self.assertTrue(result)
        self.assertIsNone(self.service.read("EXO"))

    def test_delete_nonexistent_group(self):
        result = self.service.delete("TXT")
        self.assertFalse(result)

    def test_delete_then_browse(self):
        self.service.add("BTS", 7)
        self.service.delete("BTS")
        result = self.service.browse()
        self.assertNotIn("BTS", [g.name for g in result])

if __name__ == '__main__':
    unittest.main()
