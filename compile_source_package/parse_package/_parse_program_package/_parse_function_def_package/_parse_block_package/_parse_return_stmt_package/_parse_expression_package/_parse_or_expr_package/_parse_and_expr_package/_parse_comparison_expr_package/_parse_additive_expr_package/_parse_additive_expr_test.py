import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any
import sys


Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


def create_mock_multiplicative_expr():
    """创建一个智能的 mock 函数，模拟 _parse_multiplicative_expr 的行为"""
    def mock_parse_multiplicative_expr(parser_state: ParserState) -> AST:
        """Mock 实现：返回当前 token 并递增 pos"""
        # 如果已经有错误，不消耗 token
        if parser_state.get("error"):
            return {"type": "ERROR", "value": "error", "line": 0, "column": 0}
        
        tokens = parser_state.get("tokens", [])
        pos = parser_state.get("pos", 0)
        
        if pos >= len(tokens):
            # 如果 pos 超出范围，返回一个默认值
            return {"type": "LITERAL", "value": 0, "line": 0, "column": 0}
        
        token = tokens[pos]
        # 递增 pos，模拟消耗 token
        parser_state["pos"] = pos + 1
        
        return {
            "type": token["type"],
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    return mock_parse_multiplicative_expr


# 创建 mock 函数
mock_multiplicative_expr = create_mock_multiplicative_expr()

# 创建 mock 模块用于所有依赖链中的模块
mock_module = MagicMock()
mock_module._parse_multiplicative_expr = mock_multiplicative_expr

# 注册所有可能需要的模块路径到 sys.modules
base_path = (
    "main_package.compile_source_package.parse_package._parse_program_package."
    "_parse_function_def_package._parse_block_package._parse_return_stmt_package."
    "_parse_expression_package._parse_or_expr_package._parse_and_expr_package."
    "_parse_comparison_expr_package._parse_additive_expr_package"
)

# 注册 _parse_additive_expr_src 模块中的 _parse_multiplicative_expr
multiplicative_src_path = base_path + "._parse_multiplicative_expr_package._parse_multiplicative_expr_src"
sys.modules[multiplicative_src_path] = mock_module

# 还需要 mock 依赖链中的其他模块以防止导入错误
primary_expr_path = base_path + "._parse_multiplicative_expr_package._parse_primary_expr_package._parse_primary_expr_src"
sys.modules[primary_expr_path] = mock_module

# 现在可以安全导入
from ._parse_additive_expr_src import _parse_additive_expr


class TestParseAdditiveExpr(unittest.TestCase):
    """单元测试：_parse_additive_expr 函数"""

    def _create_token(self, token_type: str, value: str, line: int, column: int) -> Token:
        """Helper: 创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> ParserState:
        """Helper: 创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_simple_addition(self):
        """测试简单加法表达式：a + b"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "a")
        self.assertEqual(result["children"][1]["value"], "b")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)

    def test_simple_subtraction(self):
        """测试简单减法表达式：a - b"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("MINUS", "-", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(len(result["children"]), 2)

    def test_multiple_operations_left_associative(self):
        """测试多个操作的左结合性：a + b - c"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("MINUS", "-", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][1]["value"], "c")
        self.assertEqual(result["children"][0]["type"], "BINARY_OP")
        self.assertEqual(result["children"][0]["value"], "+")
        self.assertEqual(parser_state["pos"], 5)

    def test_single_multiplicative_expr(self):
        """测试单个乘法表达式（无加减运算符）"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
        ])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 1)

    def test_empty_tokens(self):
        """测试空 tokens 列表"""
        parser_state = self._create_parser_state([])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 0)

    def test_error_propagation_from_multiplicative(self):
        """测试从 _parse_multiplicative_expr 传播的错误"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
        ])
        parser_state["error"] = "Parse error in multiplicative"

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["pos"], 0)

    def test_error_during_right_operand_parsing(self):
        """测试解析右操作数时发生错误"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
        ])
        
        # 保存原始 mock 函数
        original_mock = mock_multiplicative_expr
        
        # 创建一个新的 mock 函数，在第二次调用时设置错误
        call_count = [0]
        def error_mock(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                # 第一次调用，正常返回
                ps["pos"] = 1
                return {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            else:
                # 第二次调用，设置错误
                ps["error"] = "Error parsing right operand"
                return {"type": "ERROR", "value": "error", "line": 1, "column": 3}
        
        # 临时替换 mock
        import main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src as src_module
        src_module._parse_multiplicative_expr = error_mock

        result = _parse_additive_expr(parser_state)
        
        # 恢复原始 mock
        src_module._parse_multiplicative_expr = original_mock

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertTrue("error" in parser_state)

    def test_non_additive_token_stops_loop(self):
        """测试非加减运算符 token 停止循环"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("STAR", "*", 1, 3),
        ])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 1)

    def test_pos_at_end_of_tokens(self):
        """测试 pos 已在 tokens 末尾"""
        parser_state = self._create_parser_state(
            [self._create_token("IDENTIFIER", "a", 1, 1)],
            pos=1
        )

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(parser_state["pos"], 1)

    def test_mixed_additive_operators(self):
        """测试混合加减运算符：a - b + c"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("MINUS", "-", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("PLUS", "+", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ])

        result = _parse_additive_expr(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["children"][0]["value"], "-")
        self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()