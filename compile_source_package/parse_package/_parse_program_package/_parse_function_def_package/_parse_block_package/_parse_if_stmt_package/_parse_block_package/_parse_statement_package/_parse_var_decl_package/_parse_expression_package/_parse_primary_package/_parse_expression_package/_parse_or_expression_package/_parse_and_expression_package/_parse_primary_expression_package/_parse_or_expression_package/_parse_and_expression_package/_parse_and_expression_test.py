"""
单元测试文件：_parse_and_expression 函数测试
"""
import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._parse_and_expression_src import _parse_and_expression


class TestParseAndExpression(unittest.TestCase):
    """测试 _parse_and_expression 函数"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_single_comparison_no_and(self):
        """测试：单个比较表达式，无 AND 运算符"""
        mock_comparison_ast = {"type": "comparison", "value": "a > 5"}
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OPERATOR", ">"),
            self._create_token("NUMBER", "5")
        ])
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.return_value = mock_comparison_ast
            
            result = _parse_and_expression(parser_state)
            
            # 验证返回的是 comparison AST
            self.assertEqual(result, mock_comparison_ast)
            # 验证 _parse_comparison_expression 被调用一次
            mock_parse_comp.assert_called_once()
            # 验证 pos 没有变化（因为没有 AND）
            self.assertEqual(parser_state["pos"], 0)

    def test_one_and_operation(self):
        """测试：一个 AND 运算"""
        left_ast = {"type": "comparison", "value": "a > 5"}
        right_ast = {"type": "comparison", "value": "b < 10"}
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OPERATOR", ">"),
            self._create_token("NUMBER", "5"),
            self._create_token("KEYWORD", "AND", line=1, column=5),
            self._create_token("IDENTIFIER", "b"),
            self._create_token("OPERATOR", "<"),
            self._create_token("NUMBER", "10")
        ])
        
        call_count = [0]
        
        def side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_ast
            else:
                return right_ast
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            # 验证返回的是 binary_op AST
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "and")
            self.assertEqual(result["left"], left_ast)
            self.assertEqual(result["right"], right_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            # 验证 _parse_comparison_expression 被调用两次
            self.assertEqual(mock_parse_comp.call_count, 2)
            # 验证 pos 移动到 tokens 末尾
            self.assertEqual(parser_state["pos"], 7)

    def test_multiple_chained_and(self):
        """测试：多个链式 AND 运算"""
        ast1 = {"type": "comparison", "value": "a > 5"}
        ast2 = {"type": "comparison", "value": "b < 10"}
        ast3 = {"type": "comparison", "value": "c == 3"}
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OPERATOR", ">"),
            self._create_token("NUMBER", "5"),
            self._create_token("KEYWORD", "AND", line=1, column=5),
            self._create_token("IDENTIFIER", "b"),
            self._create_token("OPERATOR", "<"),
            self._create_token("NUMBER", "10"),
            self._create_token("KEYWORD", "AND", line=1, column=12),
            self._create_token("IDENTIFIER", "c"),
            self._create_token("OPERATOR", "=="),
            self._create_token("NUMBER", "3")
        ])
        
        call_count = [0]
        
        def side_effect(state):
            result = [ast1, ast2, ast3][call_count[0]]
            call_count[0] += 1
            return result
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            # 验证返回的是嵌套的 binary_op AST（左结合）
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "and")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 12)
            
            # 右侧应该是 ast3
            self.assertEqual(result["right"], ast3)
            
            # 左侧应该是另一个 binary_op (ast1 AND ast2)
            left_part = result["left"]
            self.assertEqual(left_part["type"], "binary_op")
            self.assertEqual(left_part["operator"], "and")
            self.assertEqual(left_part["left"], ast1)
            self.assertEqual(left_part["right"], ast2)
            self.assertEqual(left_part["line"], 1)
            self.assertEqual(left_part["column"], 5)
            
            # 验证 _parse_comparison_expression 被调用三次
            self.assertEqual(mock_parse_comp.call_count, 3)

    def test_empty_tokens(self):
        """测试：空 tokens 列表"""
        parser_state = self._create_parser_state([])
        mock_ast = {"type": "comparison", "value": "empty"}
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.return_value = mock_ast
            
            result = _parse_and_expression(parser_state)
            
            # 验证返回 comparison AST
            self.assertEqual(result, mock_ast)
            mock_parse_comp.assert_called_once()

    def test_error_from_comparison_expression(self):
        """测试：_parse_comparison_expression 返回错误"""
        parser_state = self._create_parser_state([
            self._create_token("INVALID", "x")
        ])
        parser_state["error"] = "parse error"
        error_ast = {"type": "error", "message": "parse error"}
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.return_value = error_ast
            
            result = _parse_and_expression(parser_state)
            
            # 验证直接返回错误 AST
            self.assertEqual(result, error_ast)
            mock_parse_comp.assert_called_once()
            # 验证没有继续解析 AND
            self.assertEqual(parser_state["pos"], 0)

    def test_and_at_end_without_right_operand(self):
        """测试：AND 在末尾，没有右操作数"""
        left_ast = {"type": "comparison", "value": "a > 5"}
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OPERATOR", ">"),
            self._create_token("NUMBER", "5"),
            self._create_token("KEYWORD", "AND", line=1, column=5)
        ])
        
        call_count = [0]
        
        def side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_ast
            else:
                # 第二次调用时设置错误（没有右操作数）
                state["error"] = "unexpected end of input"
                return {"type": "error", "message": "unexpected end of input"}
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            # 验证返回的是左边的 AST（因为右边解析出错）
            self.assertEqual(result, left_ast)
            self.assertEqual(mock_parse_comp.call_count, 2)
            # 验证错误被设置
            self.assertEqual(parser_state.get("error"), "unexpected end of input")

    def test_and_followed_by_non_comparison(self):
        """测试：AND 后面不是比较表达式（break 条件）"""
        left_ast = {"type": "comparison", "value": "a > 5"}
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OPERATOR", ">"),
            self._create_token("NUMBER", "5"),
            self._create_token("KEYWORD", "AND", line=1, column=5),
            self._create_token("KEYWORD", "IF", "if")  # 不是比较表达式开始的 token
        ])
        
        call_count = [0]
        
        def side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_ast
            else:
                # 第二次调用解析右操作数
                return {"type": "comparison", "value": "parse_if"}
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            # 验证构建了 AND 表达式
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "and")
            self.assertEqual(result["left"], left_ast)
            # 验证 _parse_comparison_expression 被调用两次
            self.assertEqual(mock_parse_comp.call_count, 2)

    def test_token_without_value_field(self):
        """测试：token 没有 value 字段"""
        mock_ast = {"type": "comparison", "value": "test"}
        
        parser_state = self._create_parser_state([
            {"type": "IDENTIFIER"},  # 没有 value 字段
        ])
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.return_value = mock_ast
            
            result = _parse_and_expression(parser_state)
            
            # 验证不会崩溃，返回 comparison AST
            self.assertEqual(result, mock_ast)
            mock_parse_comp.assert_called_once()

    def test_and_with_different_line_column(self):
        """测试：AND 运算符在不同行列位置"""
        left_ast = {"type": "comparison", "value": "a > 5"}
        right_ast = {"type": "comparison", "value": "b < 10"}
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", ">", line=1, column=3),
            self._create_token("NUMBER", "5", line=1, column=5),
            self._create_token("KEYWORD", "AND", line=2, column=10),
            self._create_token("IDENTIFIER", "b", line=2, column=14),
            self._create_token("OPERATOR", "<", line=2, column=16),
            self._create_token("NUMBER", "10", line=2, column=18)
        ])
        
        call_count = [0]
        
        def side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_ast
            else:
                return right_ast
        
        with patch("._parse_and_expression_src._parse_comparison_expression") as mock_parse_comp:
            mock_parse_comp.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            # 验证 AST 节点保留了 AND token 的行列信息
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
