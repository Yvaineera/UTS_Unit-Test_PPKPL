import unittest
from unittest.mock import patch
import io

from data.group_repository import GroupRepository
from usecases.group_service import GroupService
from interface.cli import run_cli

class TestGroupCLI(unittest.TestCase):

    def setUp(self):
        self.repo = GroupRepository()
        self.service = GroupService(self.repo)

    @patch('builtins.input', side_effect=['1', 'BTS', '7', '6'])
    def test_add_group_success(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("✅ Group added.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', 'BTS', '7', '1', 'BTS', '7', '6'])
    def test_add_duplicate_group(self, mock_input):
        self.service.add("BTS", 7)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("⚠️ Group already exists.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', '', '7', '6'])
    def test_add_group_missing_name(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("⚠️ Group already exists.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['2', '6'])
    def test_browse_existing_group(self, mock_input):
        self.service.add("BLACKPINK", 4)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("BLACKPINK", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['2', '6'])
    def test_browse_no_groups(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("⚠️ No groups found.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['2', '6'])
    def test_browse_multiple_groups(self, mock_input):
        self.service.add("EXO", 9)
        self.service.add("TWICE", 9)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            output = mock_stdout.getvalue()
            self.assertIn("EXO", output)
            self.assertIn("TWICE", output)

    @patch('builtins.input', side_effect=['3', 'BTS', '6'])
    def test_read_existing_group(self, mock_input):
        self.service.add("BTS", 7)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("🎤 BTS has 7 members.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['3', 'NCT', '6'])
    def test_read_nonexistent_group(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("❌ Group not found.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['3', '', '6'])
    def test_read_empty_input(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("❌ Group not found.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['4', 'EXO', 'EXO-CBX', '6', '6'])
    def test_edit_group_success(self, mock_input):
        self.service.add("EXO", 9)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("✅ Updated.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['4', 'FakeGroup', 'NewName', '8', '6'])
    def test_edit_nonexistent_group(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("❌ Edit failed.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['4', 'EXO', '', '', '6'])
    def test_edit_nothing_changed(self, mock_input):
        self.service.add("EXO", 9)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("✅ Updated.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['5', 'TWICE', '6'])
    def test_delete_success(self, mock_input):
        self.service.add("TWICE", 9)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("✅ Deleted.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['5', 'NonExist', '6'])
    def test_delete_nonexistent_group(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("❌ Group not found.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['5', '', '6'])
    def test_delete_empty_input(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            run_cli(self.service)
            self.assertIn("❌ Group not found.", mock_stdout.getvalue())

