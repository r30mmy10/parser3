import unittest
from config_parser import remove_comments, parse_config, parse_value, evaluate_postfix, parse_content


class TestConfigParser(unittest.TestCase):
    def test_remove_comments(self):
        input_content = """
        :: Это однострочный комментарий
        let a = 10
        /+ Это многострочный
        комментарий +/
        let b = 20
        """
        expected_output = """let a = 10
        let b = 20
        """
        self.assertEqual(remove_comments(input_content).strip(), expected_output.strip())

    def test_parse_config(self):
        # Тест на проверку базового парсинга
        parsed_content = parse_config('example_config.txt')
        self.assertIsNotNone(parsed_content)

    def test_parse_value(self):
        self.assertEqual(parse_value("'test'"), "test")
        self.assertEqual(parse_value("array(1, 2, 3)"), [1, 2, 3])
        self.assertEqual(parse_value("10"), 10)

    def test_evaluate_postfix(self):
        context = {}  # Пустой контекст для тестов без переменных
        self.assertEqual(evaluate_postfix("10 5 +", context), 15)
        self.assertEqual(evaluate_postfix("10 5 -", context), 5)
        self.assertEqual(evaluate_postfix("2 3 *", context), 6)
        self.assertEqual(evaluate_postfix("10 5 + 2 *", context), 30)

    def test_syntax_error(self):
        input_content = "let a = "
        with self.assertRaises(ValueError):
            parse_content(input_content)

    def test_parse_network_config(self):
        parsed_content = parse_config('network_config.txt')
        self.assertIsNotNone(parsed_content)
        self.assertEqual(parsed_content['hostname'], 'my-server')
        self.assertEqual(parsed_content['ip_address'], '192.168.0.1')
        self.assertEqual(parsed_content['ports'], [80, 443, 22])
        self.assertEqual(parsed_content['max_connections'], 75)


    def test_parse_user_profile_config(self):
        parsed_content = parse_config('user_profile_config.txt')
        self.assertIsNotNone(parsed_content)
        self.assertEqual(parsed_content['username'], 'Bob')
        self.assertEqual(parsed_content['age'], 30)
        self.assertEqual(parsed_content['skills'], ['Python', 'Java', 'C++'])
        self.assertEqual(parsed_content['completed_projects'], 7)


if __name__ == '__main__':
    unittest.main()
