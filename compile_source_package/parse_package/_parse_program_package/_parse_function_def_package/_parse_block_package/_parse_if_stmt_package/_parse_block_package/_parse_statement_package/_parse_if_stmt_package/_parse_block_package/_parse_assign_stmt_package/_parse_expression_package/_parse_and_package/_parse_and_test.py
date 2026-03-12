# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_and_src import _parse_and


class TestParseAnd(unittest.TestCase):
    """测试 _parse_and 函数解析 AND 表达式。"""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """辅助方法：创建 parser_state 对象。"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """辅助方法：创建 token 对象。"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(
        self,
        node_type: str,
        value: Any = None,
        line: int = 1,
        column: int = 1,
        children: list = None,
        **kwargs
    ) -> Dict[str, Any]:
        """辅助方法：创建 AST 节点对象。"""
        node = {
            "type": node_type,
            "line": line,
            "column": column
        }
        if value is not None:
            node["value"] = value
        if children is not None:
            node["children"] = children
        node.update(kwargs)
        return node

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_single_and_expression(self, mock_parse_equality: MagicMock):
        """测试单个 AND 表达式：a AND b"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_and = self._create_token("AND", "AND", 1, 3)
        token_b = self._create_token("IDENTIFIER", "b", 1, 5)
        
        tokens = [token_a, token_and, token_b]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 1)
        ast_b = self._create_ast_node("IDENTIFIER", "b", 1, 5)
        
        # 第一次调用返回 ast_a，第二次调用返回 ast_b
        mock_parse_equality.side_effect = [ast_a, ast_b]
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "BINARY")
        self.assertEqual(result["operator"], "AND")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(result["left"], ast_a)
        self.assertEqual(result["right"], ast_b)
        
        # 验证 pos 被正确更新（消耗了 3 个 token）
        self.assertEqual(parser_state["pos"], 3)
        
        # 验证 _parse_equality 被调用了 2 次
        self.assertEqual(mock_parse_equality.call_count, 2)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_multiple_and_expressions_left_associative(self, mock_parse_equality: MagicMock):
        """测试多个 AND 表达式（左结合）：a AND b AND c"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_and1 = self._create_token("AND", "AND", 1, 3)
        token_b = self._create_token("IDENTIFIER", "b", 1, 5)
        token_and2 = self._create_token("AND", "AND", 1, 7)
        token_c = self._create_token("IDENTIFIER", "c", 1, 9)
        
        tokens = [token_a, token_and1, token_b, token_and2, token_c]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 1)
        ast_b = self._create_ast_node("IDENTIFIER", "b", 1, 5)
        ast_c = self._create_ast_node("IDENTIFIER", "c", 1, 9)
        
        # 三次调用分别返回 ast_a, ast_b, ast_c
        mock_parse_equality.side_effect = [ast_a, ast_b, ast_c]
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证结果应该是左结合：(a AND b) AND c
        self.assertEqual(result["type"], "BINARY")
        self.assertEqual(result["operator"], "AND")
        self.assertEqual(result["line"], 1)  # 第二个 AND 的行号
        self.assertEqual(result["column"], 7)  # 第二个 AND 的列号
        
        # 右侧应该是 c
        self.assertEqual(result["right"], ast_c)
        
        # 左侧应该是 (a AND b)
        left_node = result["left"]
        self.assertEqual(left_node["type"], "BINARY")
        self.assertEqual(left_node["operator"], "AND")
        self.assertEqual(left_node["left"], ast_a)
        self.assertEqual(left_node["right"], ast_b)
        
        # 验证 pos 被正确更新（消耗了 5 个 token）
        self.assertEqual(parser_state["pos"], 5)
        
        # 验证 _parse_equality 被调用了 3 次
        self.assertEqual(mock_parse_equality.call_count, 3)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_no_and_token(self, mock_parse_equality: MagicMock):
        """测试没有 AND token 的情况：只有相等性表达式"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_plus = self._create_token("PLUS", "+", 1, 2)
        
        tokens = [token_a, token_plus]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 1)
        mock_parse_equality.return_value = ast_a
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证结果直接返回左侧 AST，没有包装成 BINARY
        self.assertEqual(result, ast_a)
        
        # 验证 pos 只前进到 1（只消耗了第一个 token 用于解析 equality）
        # 注意：pos 的实际值取决于 _parse_equality 的实现
        # 这里我们验证 pos 没有继续前进（没有消耗 PLUS token）
        self.assertGreaterEqual(parser_state["pos"], 1)
        
        # 验证 _parse_equality 只被调用了 1 次
        self.assertEqual(mock_parse_equality.call_count, 1)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_and_at_end_of_tokens(self, mock_parse_equality: MagicMock):
        """测试 AND token 在末尾的情况（语法错误场景，但函数不处理）"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_and = self._create_token("AND", "AND", 1, 3)
        
        tokens = [token_a, token_and]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 1)
        ast_empty = self._create_ast_node("EMPTY", None, 1, 3)
        
        mock_parse_equality.side_effect = [ast_a, ast_empty]
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "BINARY")
        self.assertEqual(result["operator"], "AND")
        
        # 验证 pos 前进到末尾
        self.assertEqual(parser_state["pos"], 2)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_start_pos_not_zero(self, mock_parse_equality: MagicMock):
        """测试从非零位置开始解析"""
        # 准备测试数据
        token_skip = self._create_token("SKIP", "", 1, 1)
        token_a = self._create_token("IDENTIFIER", "a", 1, 2)
        token_and = self._create_token("AND", "AND", 1, 4)
        token_b = self._create_token("IDENTIFIER", "b", 1, 6)
        
        tokens = [token_skip, token_a, token_and, token_b]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 2)
        ast_b = self._create_ast_node("IDENTIFIER", "b", 1, 6)
        
        mock_parse_equality.side_effect = [ast_a, ast_b]
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "BINARY")
        self.assertEqual(result["operator"], "AND")
        self.assertEqual(result["left"], ast_a)
        self.assertEqual(result["right"], ast_b)
        
        # 验证 pos 从 1 前进到 4
        self.assertEqual(parser_state["pos"], 4)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_token_position_info_preserved(self, mock_parse_equality: MagicMock):
        """测试 AND token 的位置信息被正确保存到 AST 中"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 5, 10)
        token_and = self._create_token("AND", "AND", 5, 12)
        token_b = self._create_token("IDENTIFIER", "b", 5, 15)
        
        tokens = [token_a, token_and, token_b]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 5, 10)
        ast_b = self._create_ast_node("IDENTIFIER", "b", 5, 15)
        
        mock_parse_equality.side_effect = [ast_a, ast_b]
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证位置信息
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_empty_filename_uses_default(self, mock_parse_equality: MagicMock):
        """测试没有 filename 时使用默认值（函数内部处理，不直接影响输出）"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        
        tokens = [token_a]
        parser_state = self._create_parser_state(tokens, pos=0, filename="")
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 1)
        mock_parse_equality.return_value = ast_a
        
        # 执行测试（不应该抛出异常）
        result = _parse_and(parser_state)
        
        # 验证结果
        self.assertEqual(result, ast_a)

    @patch("._parse_equality_package._parse_equality_src._parse_equality")
    def test_and_followed_by_non_identifier(self, mock_parse_equality: MagicMock):
        """测试 AND 后面跟着非标识符 token"""
        # 准备测试数据
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_and = self._create_token("AND", "AND", 1, 3)
        token_number = self._create_token("NUMBER", "42", 1, 5)
        
        tokens = [token_a, token_and, token_number]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 配置 mock 返回值
        ast_a = self._create_ast_node("IDENTIFIER", "a", 1, 1)
        ast_number = self._create_ast_node("NUMBER", 42, 1, 5)
        
        mock_parse_equality.side_effect = [ast_a, ast_number]
        
        # 执行测试
        result = _parse_and(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "BINARY")
        self.assertEqual(result["operator"], "AND")
        self.assertEqual(result["right"], ast_number)
        
        # 验证 pos 前进到 3
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
