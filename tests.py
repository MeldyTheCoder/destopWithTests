from main import check_password_hash, generate_password_hash, generate_random_number
import unittest


class TestPassword(unittest.TestCase):

    def test_password_validation(self):
        password = 'qwe123qwe3455242'
        password_hash = generate_password_hash(password)
        is_password_valid = check_password_hash(password, password_hash)

        self.assertEqual(is_password_valid, True)

        password_new = 'f3rfreferfer'
        is_password_valid = check_password_hash(password_new, password_hash)

        self.assertEqual(is_password_valid, False)


class TestRandom(unittest.TestCase):
    def test_random_value_generation(self):
        from_value, to_value = 0, 2
        random_value = generate_random_number(from_value, to_value)

        self.assertGreaterEqual(random_value, from_value)
        self.assertLessEqual(random_value, to_value)

        from_value, to_value = -1, -2
        with self.assertRaises(ValueError):
            generate_random_number(from_value, to_value)


if __name__ == '__main__':
    unittest.main()

