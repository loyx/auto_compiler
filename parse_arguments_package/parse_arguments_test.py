import unittest
from .parse_arguments_src import parse_arguments


class TestParseArguments(unittest.TestCase):
    """测试 parse_arguments 函数的命令行参数解析逻辑"""

    def test_basic_source_file_only(self):
        """测试仅指定源文件的基本场景"""
        config = parse_arguments(["main.c"])
        self.assertEqual(config["source_file"], "main.c")
        self.assertIsNone(config["output_file"])
        self.assertFalse(config["verbose"])

    def test_with_output_file_option(self):
        """测试使用 -o 选项指定输出文件"""
        config = parse_arguments(["main.c", "-o", "out.exe"])
        self.assertEqual(config["source_file"], "main.c")
        self.assertEqual(config["output_file"], "out.exe")
        self.assertFalse(config["verbose"])

    def test_with_verbose_flag(self):
        """测试使用 -v 标志启用详细输出"""
        config = parse_arguments(["main.c", "-v"])
        self.assertEqual(config["source_file"], "main.c")
        self.assertIsNone(config["output_file"])
        self.assertTrue(config["verbose"])

    def test_with_both_options(self):
        """测试同时使用 -o 和 -v 选项"""
        config = parse_arguments(["main.c", "-o", "out.exe", "-v"])
        self.assertEqual(config["source_file"], "main.c")
        self.assertEqual(config["output_file"], "out.exe")
        self.assertTrue(config["verbose"])

    def test_flags_before_source_file(self):
        """测试标志可以出现在源文件之前"""
        config = parse_arguments(["-v", "main.c", "-o", "out.exe"])
        self.assertEqual(config["source_file"], "main.c")
        self.assertEqual(config["output_file"], "out.exe")
        self.assertTrue(config["verbose"])

    def test_flags_after_source_file(self):
        """测试标志可以出现在源文件之后"""
        config = parse_arguments(["main.c", "-v", "-o", "out.exe"])
        self.assertEqual(config["source_file"], "main.c")
        self.assertEqual(config["output_file"], "out.exe")
        self.assertTrue(config["verbose"])

    def test_empty_args_raises_error(self):
        """测试空参数列表抛出 ValueError"""
        with self.assertRaises(ValueError):
            parse_arguments([])

    def test_missing_source_file_raises_error(self):
        """测试仅有标志而无源文件时抛出 ValueError"""
        with self.assertRaises(ValueError):
            parse_arguments(["-v"])

    def test_o_without_file_raises_error(self):
        """测试 -o 后无文件路径时抛出 ValueError"""
        with self.assertRaises(ValueError):
            parse_arguments(["main.c", "-o"])

    def test_unknown_flag_raises_error(self):
        """测试未知标志抛出 ValueError"""
        with self.assertRaises(ValueError):
            parse_arguments(["main.c", "-unknown"])

    def test_multiple_source_files_raises_error(self):
        """测试多个源文件抛出 ValueError"""
        with self.assertRaises(ValueError):
            parse_arguments(["main.c", "other.c"])

    def test_error_message_o_without_file(self):
        """测试 -o 无文件时的错误消息包含正确提示"""
        with self.assertRaises(ValueError) as context:
            parse_arguments(["main.c", "-o"])
        self.assertIn("选项 -o 后必须指定输出文件路径", str(context.exception))

    def test_error_message_unknown_flag(self):
        """测试未知标志的错误消息包含标志名称"""
        with self.assertRaises(ValueError) as context:
            parse_arguments(["main.c", "-unknown"])
        self.assertIn("-unknown", str(context.exception))

    def test_error_message_missing_source(self):
        """测试缺少源文件的错误消息包含正确提示"""
        with self.assertRaises(ValueError) as context:
            parse_arguments(["-v"])
        self.assertIn("必须指定源文件路径", str(context.exception))

    def test_error_message_multiple_sources(self):
        """测试多个源文件的错误消息包含正确提示"""
        with self.assertRaises(ValueError) as context:
            parse_arguments(["main.c", "other.c"])
        self.assertIn("只能指定一个源文件", str(context.exception))


if __name__ == "__main__":
    unittest.main()
