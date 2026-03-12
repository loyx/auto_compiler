import unittest
from unittest.mock import patch


class TestGenerateFunctionCode(unittest.TestCase):
    """测试 generate_function_code 函数"""
    
    def setUp(self):
        """设置测试夹具"""
        self.sample_func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": ["x", "y"],
            "return_type": "int",
            "body": []
        }
        self.sample_label_counter = {
            "if_else": 0,
            "if_end": 0,
            "while_cond": 0,
            "while_end": 0,
            "for_cond": 0,
            "for_end": 0,
            "for_update": 0,
        }
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_basic_function_generation(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试基本函数生成 - 空函数体"""
        mock_calc_stack.return_value = 48
        mock_prologue.return_value = "    prologue_code"
        mock_epilogue.return_value = "    epilogue_code"
        mock_build_offsets.return_value = ({"x": 16, "y": 24}, 32)
        mock_stmt_code.return_value = "    statement_code"
        
        from .generate_function_code_src import generate_function_code
        result = generate_function_code(self.sample_func_def, self.sample_label_counter)
        
        self.assertIn("test_func:", result)
        self.assertIn("prologue_code", result)
        self.assertIn("epilogue_code", result)
        self.assertIn("test_func_exit:", result)
        mock_calc_stack.assert_called_once()
        mock_prologue.assert_called_once_with("test_func", 48)
        mock_epilogue.assert_called_once_with(48)
        mock_build_offsets.assert_called_once_with(["x", "y"], 16)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_void_function_no_default_return(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试 void 函数不添加默认返回"""
        mock_calc_stack.return_value = 48
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = self.sample_func_def.copy()
        func_def["body"] = []
        func_def["return_type"] = "void"
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        self.assertIn("test_func:", result)
        self.assertIn("test_func_exit:", result)
        self.assertNotIn("mov x0, #0", result)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_non_void_without_explicit_return(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试非 void 函数无显式返回时添加默认返回"""
        mock_calc_stack.return_value = 48
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": [],
            "return_type": "int",
            "body": [
                {"type": "VAR_DECL", "name": "x"}
            ]
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        self.assertIn("mov x0, #0", result)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_non_void_with_explicit_return(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试非 void 函数有显式返回时不添加默认返回"""
        mock_calc_stack.return_value = 48
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": [],
            "return_type": "int",
            "body": [
                {"type": "RETURN", "value": {"type": "LITERAL", "value": 42}}
            ]
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        self.assertNotIn("mov x0, #0", result)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_function_with_params(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试带参数的函数"""
        mock_calc_stack.return_value = 64
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({"x": 16, "y": 24}, 32)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "add",
            "params": ["x", "y"],
            "return_type": "int",
            "body": []
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        mock_build_offsets.assert_called_once_with(["x", "y"], 16)
        self.assertIn("add:", result)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_function_with_body_statements(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试带函数体语句的函数"""
        mock_calc_stack.return_value = 48
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.side_effect = ["    stmt1", "    stmt2", "    stmt3"]
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": [],
            "return_type": "void",
            "body": [
                {"type": "ASSIGN"},
                {"type": "IF"},
                {"type": "WHILE"}
            ]
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        self.assertEqual(mock_stmt_code.call_count, 3)
        self.assertIn("stmt1", result)
        self.assertIn("stmt2", result)
        self.assertIn("stmt3", result)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_stack_size_calculation(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试栈帧大小计算调用"""
        mock_calc_stack.return_value = 80
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": ["a", "b", "c"],
            "return_type": "void",
            "body": [
                {"type": "VAR_DECL", "name": "x"},
                {"type": "VAR_DECL", "name": "y"}
            ]
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        mock_calc_stack.assert_called_once_with(3, 2)
        mock_prologue.assert_called_once_with("test_func", 80)
        mock_epilogue.assert_called_once_with(80)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_output_format(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试输出格式为换行分隔的字符串"""
        mock_calc_stack.return_value = 48
        mock_prologue.return_value = "    prologue_line"
        mock_epilogue.return_value = "    epilogue_line"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    body_line"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": [],
            "return_type": "void",
            "body": [{"type": "ASSIGN"}]
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        lines = result.split("\n")
        self.assertEqual(lines[0], "test_func:")
        self.assertIn("    prologue_line", lines)
        self.assertIn("    body_line", lines)
        self.assertIn("test_func_exit:", lines)
        self.assertIn("    epilogue_line", lines)
    
    @patch('generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_empty_params_list(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试无参数函数"""
        mock_calc_stack.return_value = 32
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "no_param_func",
            "params": [],
            "return_type": "void",
            "body": []
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        mock_build_offsets.assert_called_once_with([], 16)
        self.assertIn("no_param_func:", result)
    
    @patch('generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_missing_body_key(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试缺少 body 键的情况"""
        mock_calc_stack.return_value = 32
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": [],
            "return_type": "void"
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        self.assertEqual(mock_stmt_code.call_count, 0)
        self.assertIn("test_func:", result)
        self.assertIn("test_func_exit:", result)
    
    @patch('generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_missing_params_key(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试缺少 params 键的情况"""
        mock_calc_stack.return_value = 32
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "return_type": "void",
            "body": []
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        mock_build_offsets.assert_called_once_with([], 16)
    
    @patch('generate_function_code_package.generate_function_code_src.generate_statement_code')
    @patch('generate_function_code_package.generate_function_code_src.build_var_offsets')
    @patch('generate_function_code_package.generate_function_code_src.generate_prologue')
    @patch('generate_function_code_package.generate_function_code_src.generate_epilogue')
    @patch('generate_function_code_package.generate_function_code_src.calculate_stack_size')
    def test_missing_return_type_key(self, mock_calc_stack, mock_epilogue, mock_prologue, mock_build_offsets, mock_stmt_code):
        """测试缺少 return_type 键的情况（默认 void）"""
        mock_calc_stack.return_value = 32
        mock_prologue.return_value = "    prologue"
        mock_epilogue.return_value = "    epilogue"
        mock_build_offsets.return_value = ({}, 16)
        mock_stmt_code.return_value = "    stmt"
        
        from .generate_function_code_src import generate_function_code
        func_def = {
            "type": "FUNCTION_DEF",
            "name": "test_func",
            "params": [],
            "body": []
        }
        
        result = generate_function_code(func_def, self.sample_label_counter)
        
        self.assertNotIn("mov x0, #0", result)


if __name__ == "__main__":
    unittest.main()
