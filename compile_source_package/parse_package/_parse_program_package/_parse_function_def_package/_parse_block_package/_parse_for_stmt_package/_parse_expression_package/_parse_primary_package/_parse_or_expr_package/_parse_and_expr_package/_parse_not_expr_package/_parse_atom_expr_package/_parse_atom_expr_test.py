"""单元测试：_parse_atom_expr 原子表达式解析函数"""
import unittest
from typing import Dict, Any

# 相对导入被测模块
from ._parse_atom_expr_src import _parse_atom_expr


def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """辅助函数：创建 token 字典"""
    return {"type": token_type, "value": value, "line": line, "column": column}


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
    """辅助函数：创建 parser_state 字典"""
    return {"tokens": tokens, "pos": pos, "filename": filename}


class TestParseAtomExpr(unittest.TestCase):
    """_parse_atom_expr 函数测试类"""

    def test_parse_identifier(self):
        """测试解析标识符"""
        tokens = [make_token("IDENTIFIER", "x", 1, 5)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        self.assertEqual(state["pos"], 1)
        self.assertNotIn("error", state)

    def test_parse_number_integer(self):
        """测试解析整数字面量"""
        tokens = [make_token("NUMBER", "42", 2, 10)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(state["pos"], 1)

    def test_parse_number_float(self):
        """测试解析浮点数字面量"""
        tokens = [make_token("NUMBER", "3.14", 1, 1)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_string(self):
        """测试解析字符串字面量"""
        tokens = [make_token("STRING", '"hello"', 3, 7)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertEqual(state["pos"], 1)

    def test_parse_string_empty(self):
        """测试解析空字符串"""
        tokens = [make_token("STRING", '""', 1, 1)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "")
        self.assertEqual(state["pos"], 1)

    def test_parse_true(self):
        """测试解析 TRUE 关键字"""
        tokens = [make_token("TRUE", "true", 1, 1)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_false(self):
        """测试解析 FALSE 关键字"""
        tokens = [make_token("FALSE", "false", 2, 3)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)
        self.assertEqual(state["pos"], 1)

    def test_parse_paren_simple(self):
        """测试解析简单括号表达式"""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2),
            make_token("RPAREN", ")", 1, 3)
        ]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 3)
        self.assertIn("value", result)
        self.assertEqual(result["value"]["start"], 1)
        self.assertEqual(result["value"]["end"], 2)

    def test_parse_paren_nested(self):
        """测试解析嵌套括号表达式"""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("LPAREN", "(", 1, 2),
            make_token("IDENTIFIER", "x", 1, 3),
            make_token("RPAREN", ")", 1, 4),
            make_token("RPAREN", ")", 1, 5)
        ]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(state["pos"], 5)
        self.assertEqual(result["value"]["start"], 1)
        self.assertEqual(result["value"]["end"], 4)

    def test_empty_input(self):
        """测试空输入（无 tokens）"""
        state = make_parser_state([], 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "EMPTY")
        self.assertEqual(result["value"], None)
        self.assertEqual(state["pos"], 0)
        self.assertIn("error", state)
        self.assertEqual(state["error"], "Unexpected end of input")

    def test_pos_beyond_tokens(self):
        """测试 pos 超出 tokens 范围"""
        tokens = [make_token("IDENTIFIER", "x", 1, 1)]
        state = make_parser_state(tokens, 5)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "EMPTY")
        self.assertIn("error", state)
        self.assertEqual(state["error"], "Unexpected end of input")

    def test_unmatched_parenthesis(self):
        """测试未匹配的括号"""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2)
        ]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "EMPTY")
        self.assertIn("error", state)
        self.assertEqual(state["error"], "Unmatched parenthesis")

    def test_unexpected_token(self):
        """测试意外 token 类型"""
        tokens = [make_token("PLUS", "+", 1, 1)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        self.assertEqual(result["type"], "EMPTY")
        self.assertEqual(result["value"], None)
        self.assertIn("error", state)
        self.assertEqual(state["error"], "Unexpected token '+'")

    def test_multiple_expressions_sequence(self):
        """测试连续解析多个原子表达式"""
        tokens = [
            make_token("IDENTIFIER", "x", 1, 1),
            make_token("NUMBER", "42", 1, 3),
            make_token("STRING", '"test"', 1, 6)
        ]
        state = make_parser_state(tokens, 0)
        
        # 解析第一个
        result1 = _parse_atom_expr(state)
        self.assertEqual(result1["type"], "IDENTIFIER")
        self.assertEqual(result1["value"], "x")
        self.assertEqual(state["pos"], 1)
        
        # 解析第二个
        result2 = _parse_atom_expr(state)
        self.assertEqual(result2["type"], "LITERAL")
        self.assertEqual(result2["value"], 42)
        self.assertEqual(state["pos"], 2)
        
        # 解析第三个
        result3 = _parse_atom_expr(state)
        self.assertEqual(result3["type"], "LITERAL")
        self.assertEqual(result3["value"], "test")
        self.assertEqual(state["pos"], 3)

    def test_ast_node_structure(self):
        """测试 AST 节点结构完整性"""
        tokens = [make_token("IDENTIFIER", "var", 5, 12)]
        state = make_parser_state(tokens, 0)
        result = _parse_atom_expr(state)
        
        # 验证所有必需字段存在
        self.assertIn("type", result)
        self.assertIn("children", result)
        self.assertIn("value", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        
        # 验证类型
        self.assertIsInstance(result["children"], list)
        self.assertIsInstance(result["line"], int)
        self.assertIsInstance(result["column"], int)


if __name__ == "__main__":
    unittest.main()
