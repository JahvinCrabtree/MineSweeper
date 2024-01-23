import unittest
from minesweeper import MinesweeperGame, MinesweeperField, WIDTH, HEIGHT
import pygame
from unittest.mock import patch

class TestMinesweeperField(unittest.TestCase):
    def test_field_initialization(self):
        # Test the initialization of MinesweeperField
        rows, cols, mines = 5, 5, 5
        field = MinesweeperField(rows, cols, mines)

        # Check if the field has the correct dimensions
        self.assertEqual(len(field.field), rows)
        self.assertEqual(len(field.field[0]), cols)

        # Check if the correct number of mines is present in the field
        mine_count = sum(row.count(-1) for row in field.field)
        self.assertEqual(mine_count, mines)

if __name__ == '__main__':
    unittest.main()