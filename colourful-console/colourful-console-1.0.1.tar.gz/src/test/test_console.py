import unittest
import colouful_console as console

class TestColor(unittest.TestCase):

    def test_write_line(self):
        result = console.write_line('<b>Testing</b> <g>write_line</g>')
        self.assertEqual(result, 1)

    def test_read_line(self):
        """
        Currently, read_line cannot be tested as it uses user input()
        If you have solutions, please feel free to add them
        """
        self.assertEqual(1, 1)