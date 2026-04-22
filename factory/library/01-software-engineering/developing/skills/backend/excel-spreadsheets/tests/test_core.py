import unittest
from ..core import ExcelSpreadsheets

class TestExcelSpreadsheets(unittest.TestCase):
    def setUp(self):
        self.skill = ExcelSpreadsheets()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
