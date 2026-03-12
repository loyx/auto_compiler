import unittest

# Relative import from the same package
from .build_var_offsets_src import build_var_offsets


class TestBuildVarOffsets(unittest.TestCase):
    """Test cases for build_var_offsets function."""
    
    def test_empty_params(self):
        """Test with empty parameter list."""
        var_offsets, next_offset = build_var_offsets([], 16)
        self.assertEqual(var_offsets, {})
        self.assertEqual(next_offset, 16)
    
    def test_single_parameter(self):
        """Test with single parameter."""
        params = [{"name": "x", "type": "int"}]
        var_offsets, next_offset = build_var_offsets(params, 16)
        self.assertEqual(var_offsets, {"x": 16})
        self.assertEqual(next_offset, 24)
    
    def test_multiple_parameters(self):
        """Test with multiple parameters."""
        params = [
            {"name": "x", "type": "int"},
            {"name": "y", "type": "int"},
            {"name": "z", "type": "int"}
        ]
        var_offsets, next_offset = build_var_offsets(params, 16)
        self.assertEqual(var_offsets, {"x": 16, "y": 24, "z": 32})
        self.assertEqual(next_offset, 40)
    
    def test_zero_start_offset(self):
        """Test with zero start offset."""
        params = [{"name": "a", "type": "int"}]
        var_offsets, next_offset = build_var_offsets(params, 0)
        self.assertEqual(var_offsets, {"a": 0})
        self.assertEqual(next_offset, 8)
    
    def test_large_start_offset(self):
        """Test with large start offset."""
        params = [{"name": "param", "type": "int"}]
        var_offsets, next_offset = build_var_offsets(params, 1024)
        self.assertEqual(var_offsets, {"param": 1024})
        self.assertEqual(next_offset, 1032)
    
    def test_different_param_types(self):
        """Test with different parameter types (all get 8 bytes)."""
        params = [
            {"name": "int_param", "type": "int"},
            {"name": "float_param", "type": "float"},
            {"name": "ptr_param", "type": "pointer"},
            {"name": "struct_param", "type": "struct"}
        ]
        var_offsets, next_offset = build_var_offsets(params, 16)
        expected = {
            "int_param": 16,
            "float_param": 24,
            "ptr_param": 32,
            "struct_param": 40
        }
        self.assertEqual(var_offsets, expected)
        self.assertEqual(next_offset, 48)
    
    def test_offset_calculation_accuracy(self):
        """Test that offset calculation is accurate for many parameters."""
        num_params = 10
        params = [{"name": f"p{i}", "type": "int"} for i in range(num_params)]
        var_offsets, next_offset = build_var_offsets(params, 16)
        
        for i in range(num_params):
            expected_offset = 16 + i * 8
            self.assertEqual(var_offsets[f"p{i}"], expected_offset)
        
        self.assertEqual(next_offset, 16 + num_params * 8)
    
    def test_return_type(self):
        """Test that return type is tuple."""
        params = [{"name": "x", "type": "int"}]
        result = build_var_offsets(params, 16)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], int)


if __name__ == "__main__":
    unittest.main()
