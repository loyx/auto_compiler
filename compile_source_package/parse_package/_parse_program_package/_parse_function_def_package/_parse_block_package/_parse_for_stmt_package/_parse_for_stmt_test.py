# === test file for _parse_for_stmt ===
import unittest
from unittest.mock import patch

# === import using relative path ===
from ._parse_for_stmt_src import _parse_for_stmt


class TestParseForStmt(unittest.TestCase):
    """单元测试：_parse_for_stmt 函数"""

    def _create_parser_state(self, tokens, pos=0, filename="test.py"):
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type, value="", line=1, column=1):
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_happy_path_basic_for_loop(self):
        """测试：基本的 for 循环解析"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENTIFIER", "i", 1, 5),
            self._create_token("IN", "in", 1, 7),
            self._create_token("IDENTIFIER", "range", 1, 10),
            self._create_token("LPAREN", "(", 1, 15),
            self._create_token("NUMBER", "10", 1, 16),
            self._create_token("RPAREN", ")", 1, 18),
            self._create_token("COLON", ":", 1, 19),
            self._create_token("INDENT", "", 2, 1),
            self._create_token("IDENTIFIER", "print", 2, 5),
            self._create_token("LPAREN", "(", 2, 10),
            self._create_token("IDENTIFIER", "i", 2, 11),
            self._create_token("RPAREN", ")", 2, 12),
            self._create_token("NEWLINE", "", 2, 13),
            self._create_token("DEDENT", "", 3, 1),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        mock_iterable_node = {
            "type": "EXPR_STMT",
            "value": "range(10)",
            "line": 1,
            "column": 10,
            "children": []
        }
        
        mock_body_node = {
            "type": "BLOCK",
            "value": None,
            "line": 2,
            "column": 1,
            "children": []
        }
        
        with patch("._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_iterable_node
            mock_parse_block.return_value = mock_body_node
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 3)
            
            # 检查 variable_node
            variable_node = result["children"][0]
            self.assertEqual(variable_node["type"], "IDENTIFIER")
            self.assertEqual(variable_node["value"], "i")
            self.assertEqual(variable_node["line"], 1)
            self.assertEqual(variable_node["column"], 5)
            
            # 检查 iterable_node
            self.assertEqual(result["children"][1], mock_iterable_node)
            
            # 检查 body_node
            self.assertEqual(result["children"][2], mock_body_node)
            
            # 验证 parser_state pos 被更新
            self.assertEqual(parser_state["pos"], len(tokens))
            
            # 验证依赖函数被调用
            mock_parse_expr.assert_called_once()
            mock_parse_block.assert_called_once()

    def test_missing_for_token(self):
        """测试：缺少 FOR token 时抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENTIFIER", "i", 1, 1),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR token", str(context.exception))

    def test_missing_identifier_after_for(self):
        """测试：FOR 后缺少标识符时抛出 SyntaxError"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IN", "in", 1, 5),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected IDENTIFIER after FOR", str(context.exception))

    def test_missing_in_token(self):
        """测试：缺少 IN token 时抛出 SyntaxError"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENTIFIER", "i", 1, 5),
            self._create_token("COLON", ":", 1, 7),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected IN token", str(context.exception))

    def test_missing_colon_after_iterable(self):
        """测试：可迭代对象后缺少 COLON 时抛出 SyntaxError"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENTIFIER", "i", 1, 5),
            self._create_token("IN", "in", 1, 7),
            self._create_token("IDENTIFIER", "range", 1, 10),
            self._create_token("LPAREN", "(", 1, 15),
            self._create_token("NUMBER", "10", 1, 16),
            self._create_token("RPAREN", ")", 1, 18),
            self._create_token("NEWLINE", "", 1, 19),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        mock_iterable_node = {
            "type": "EXPR_STMT",
            "value": "range(10)",
            "line": 1,
            "column": 10,
            "children": []
        }
        
        with patch("._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_iterable_node
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 7}) or mock_iterable_node
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
            
            self.assertIn("Expected COLON", str(context.exception))

    def test_empty_tokens(self):
        """测试：空 tokens 列表时抛出 SyntaxError"""
        tokens = []
        
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR token", str(context.exception))

    def test_for_at_end_of_tokens(self):
        """测试：FOR 是最后一个 token 时抛出 SyntaxError"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected IDENTIFIER after FOR", str(context.exception))

    def test_for_with_complex_iterable_expression(self):
        """测试：for 循环带复杂可迭代对象表达式"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENTIFIER", "item", 1, 5),
            self._create_token("IN", "in", 1, 10),
            self._create_token("IDENTIFIER", "my_list", 1, 13),
            self._create_token("LBRACKET", "[", 1, 20),
            self._create_token("COLON", ":", 1, 21),
            self._create_token("NUMBER", "5", 1, 22),
            self._create_token("RBRACKET", "]", 1, 23),
            self._create_token("COLON", ":", 1, 24),
            self._create_token("INDENT", "", 2, 1),
            self._create_token("DEDENT", "", 3, 1),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        mock_iterable_node = {
            "type": "EXPR_STMT",
            "value": "my_list[:5]",
            "line": 1,
            "column": 13,
            "children": []
        }
        
        mock_body_node = {
            "type": "BLOCK",
            "value": None,
            "line": 2,
            "column": 1,
            "children": []
        }
        
        with patch("._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_iterable_node
            mock_parse_block.return_value = mock_body_node
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertEqual(result["children"][0]["value"], "item")
            self.assertEqual(result["children"][1], mock_iterable_node)
            self.assertEqual(result["children"][2], mock_body_node)

    def test_for_with_nested_block(self):
        """测试：for 循环带嵌套块"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENTIFIER", "i", 1, 5),
            self._create_token("IN", "in", 1, 7),
            self._create_token("IDENTIFIER", "range", 1, 10),
            self._create_token("LPAREN", "(", 1, 15),
            self._create_token("NUMBER", "10", 1, 16),
            self._create_token("RPAREN", ")", 1, 18),
            self._create_token("COLON", ":", 1, 19),
            self._create_token("INDENT", "", 2, 1),
            self._create_token("FOR", "for", 2, 5),
            self._create_token("DEDENT", "", 3, 1),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        mock_iterable_node = {
            "type": "EXPR_STMT",
            "value": "range(10)",
            "line": 1,
            "column": 10,
            "children": []
        }
        
        mock_body_node = {
            "type": "BLOCK",
            "value": None,
            "line": 2,
            "column": 1,
            "children": [
                {
                    "type": "FOR_STMT",
                    "value": None,
                    "line": 2,
                    "column": 5,
                    "children": []
                }
            ]
        }
        
        with patch("._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_iterable_node
            mock_parse_block.return_value = mock_body_node
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertEqual(len(result["children"][2]["children"]), 1)

    def test_parser_state_pos_updated_correctly(self):
        """测试：parser_state 的 pos 被正确更新"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENTIFIER", "i", 1, 5),
            self._create_token("IN", "in", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 10),
            self._create_token("COLON", ":", 1, 11),
            self._create_token("INDENT", "", 2, 1),
            self._create_token("DEDENT", "", 3, 1),
        ]
        
        parser_state = self._create_parser_state(tokens)
        
        mock_iterable_node = {
            "type": "EXPR_STMT",
            "value": "x",
            "line": 1,
            "column": 10,
            "children": []
        }
        
        mock_body_node = {
            "type": "BLOCK",
            "value": None,
            "line": 2,
            "column": 1,
            "children": []
        }
        
        def mock_parse_expression(state):
            state["pos"] = 4  # 指向 COLON
            return mock_iterable_node
        
        def mock_parse_block(state):
            state["pos"] = len(tokens)  # 指向末尾
            return mock_body_node
        
        with patch("._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.side_effect = mock_parse_expression
            mock_parse_block.side_effect = mock_parse_block
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(parser_state["pos"], len(tokens))


if __name__ == "__main__":
    unittest.main()
