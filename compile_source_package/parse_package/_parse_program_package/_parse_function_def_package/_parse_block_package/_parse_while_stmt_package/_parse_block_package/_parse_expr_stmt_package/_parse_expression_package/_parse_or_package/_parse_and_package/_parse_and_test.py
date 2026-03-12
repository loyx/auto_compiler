import unittest
from unittest.mock import patch
from ._parse_and_src import _parse_and


class TestParseAnd(unittest.TestCase):
    
    def test_single_expression_no_and(self):
        """测试没有 AND 运算符的单个表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_not_side_effect(state):
            state["pos"] = 1
            return mock_result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            mock_parse_not.assert_called_once()
    
    def test_multiple_and_expressions_left_associative(self):
        """测试多个 AND 运算符的左结合性"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
                {"type": "AND", "value": "and", "line": 1, "column": 11},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_results = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 15}
        ]
        
        call_count = [0]
        def mock_parse_not_side_effect(state):
            result = mock_results[call_count[0]]
            call_count[0] += 1
            state["pos"] = state["pos"] + 1
            return result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "and")
            self.assertEqual(len(result["children"]), 2)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "and")
            
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "IDENTIFIER")
            self.assertEqual(right_child["value"], "c")
            
            self.assertEqual(mock_parse_not.call_count, 3)
    
    def test_empty_tokens(self):
        """测试空 tokens 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_result = {
            "type": "EMPTY",
            "value": None,
            "line": 0,
            "column": 0
        }
        
        def mock_parse_not_side_effect(state):
            return mock_result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "EMPTY")
            mock_parse_not.assert_called_once()
    
    def test_and_at_end_without_right_operand(self):
        """测试 AND 在末尾没有右操作数的情况"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_results = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "EMPTY", "value": None, "line": 1, "column": 3}
        ]
        
        call_count = [0]
        def mock_parse_not_side_effect(state):
            result = mock_results[call_count[0]]
            call_count[0] += 1
            if state["pos"] < len(state["tokens"]):
                state["pos"] = state["pos"] + 1
            return result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "and")
            self.assertEqual(len(result["children"]), 2)
    
    def test_non_and_token_after_expression(self):
        """测试表达式后跟非 AND token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_not_side_effect(state):
            state["pos"] = 1
            return mock_result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            mock_parse_not.assert_called_once()
    
    def test_parser_state_pos_update(self):
        """测试 parser_state 的 pos 正确更新"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_results = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7}
        ]
        
        call_count = [0]
        def mock_parse_not_side_effect(state):
            result = mock_results[call_count[0]]
            call_count[0] += 1
            state["pos"] = state["pos"] + 1
            return result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(result["type"], "BINARY_OP")
    
    def test_ast_node_line_column_from_and_token(self):
        """测试 AST 节点的 line 和 column 来自 AND token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_results = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 10}
        ]
        
        call_count = [0]
        def mock_parse_not_side_effect(state):
            result = mock_results[call_count[0]]
            call_count[0] += 1
            state["pos"] = state["pos"] + 1
            return result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
    
    def test_default_filename_when_not_provided(self):
        """测试未提供 filename 时使用默认值"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "error": ""
        }
        
        mock_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_not_side_effect(state):
            state["pos"] = 1
            return mock_result
        
        with patch("._parse_not_package._parse_not_src._parse_not") as mock_parse_not:
            mock_parse_not.side_effect = mock_parse_not_side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            mock_parse_not.assert_called_once()


if __name__ == "__main__":
    unittest.main()
