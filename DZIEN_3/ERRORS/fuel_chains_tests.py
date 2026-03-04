import unittest

from fuel_chains import parse_command, InvalidCommandError


class TestParseCommand(unittest.TestCase):

    def test_liters_ok(self):
        liters = parse_command("10.5", 6.49)
        self.assertAlmostEqual(liters, 10.5)

    def test_pln_ok(self):
        liters = parse_command("pln 64.90", 6.49)
        self.assertAlmostEqual(liters, 10.0)

    def test_empty_input(self):
        with self.assertRaises(InvalidCommandError):
            parse_command("", 6.49)

    def test_pln_missing_amount(self):
        with self.assertRaises(InvalidCommandError):
            parse_command("pln", 6.49)

    def test_pln_amount_not_number(self):
        with self.assertRaises(InvalidCommandError) as ctx:
            parse_command("pln abc", 6.49)
        self.assertIn("musi być liczbą", str(ctx.exception))

    def test_liters_not_number(self):
        with self.assertRaises(InvalidCommandError) as ctx:
            parse_command("abc", 6.49)
        self.assertIn("Podaj liczbę litrów", str(ctx.exception))

    def test_unknown_format(self):
        with self.assertRaises(InvalidCommandError):
            parse_command("pln 100 extra", 6.49)


if __name__ == "__main__":
    unittest.main()
