import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from tree_builder import EmployeeNode, TeamTree, company_directory


class DirectoryTests(unittest.TestCase):
    def setUp(self):
        self.tree = TeamTree()
        self.output = io.StringIO()
        self.capture = redirect_stdout(self.output)
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)

    def test_initial_state(self):
        self.assertIsNone(self.tree.root)
        node = EmployeeNode('John')
        self.assertEqual(node.name, 'John')
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_recursive_insertion_and_printing(self):
        self.tree.root = EmployeeNode('Jordan')
        for manager, name, side in (
            ('Jordan', 'Taylor', 'right'), ('Jordan', 'Riley', 'left'),
            ('Riley', 'Dana', 'right'), ('Riley', 'Morgan', 'left'),
            ('Taylor', 'Alex', 'right'),
        ):
            self.tree.insert(manager, name, side)
        self.assertEqual(self.tree.root.right.right.name, 'Alex')
        self.output.seek(0)
        self.output.truncate(0)
        self.tree.print_tree()
        self.assertEqual(self.output.getvalue(),
                         '- Jordan\n  - Riley\n    - Morgan\n    - Dana\n  - Taylor\n    - Alex\n')

    def test_errors_preserve_tree(self):
        self.tree.insert('Absent', 'New', 'left')
        self.tree.print_tree()
        self.tree.root = EmployeeNode('Jordan')
        self.tree.insert('Jordan', 'Riley', ' LEFT ')
        self.tree.insert('Jordan', 'Replacement', 'left')
        self.tree.insert('Absent', 'New', 'right')
        self.tree.insert('Jordan', 'New', 'up')
        self.tree.insert('Jordan', '   ', 'right')
        self.assertEqual(self.tree.root.left.name, 'Riley')
        self.assertIsNone(self.tree.root.right)
        self.assertEqual(self.output.getvalue().count("manager 'Absent' does not exist"), 1)
        self.assertIn('already occupied', self.output.getvalue())

    def test_cli(self):
        answers = ['1', 'Jordan', '1', '2', 'Jordan', 'Riley', 'left', '3', 'bad', '4']
        with patch('builtins.input', side_effect=answers):
            company_directory()
        output = self.output.getvalue()
        self.assertIn('Team lead already exists', output)
        self.assertIn('- Jordan\n  - Riley', output)
        self.assertIn('Invalid option', output)
        self.assertIn('Good Bye!', output)


if __name__ == '__main__':
    unittest.main()
