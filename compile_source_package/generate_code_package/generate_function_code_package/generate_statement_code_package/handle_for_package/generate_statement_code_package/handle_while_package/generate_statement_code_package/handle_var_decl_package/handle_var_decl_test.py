from typing import Dict
import unittest

# Relative import from the same package
from .handle_var_decl_src import handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for handle_var_decl function."""
    
    def test_var_decl_without_init(self):
        """Test variable declaration without initialization."""
        stmt = {"type": "VAR_DECL", "name": "x"}
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        assembly_code, updated_offset = handle_var_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )
        
        # Verify offset updated correctly
        self.assertEqual(updated_offset, 4)
        
        # Verify var_offsets updated in-place
        self.assertIn("x", var_offsets)
        self.assertEqual(var_offsets["x"], 0)
        
        # Verify assembly code contains declaration comment
        self.assertIn("@ declare variable x at offset 0", assembly_code)
        
        # Verify no initialization code since init is not present
        self.assertNotIn("MOV r0", assembly_code)
        self.assertNotIn("STR r0", assembly_code)
    
    def test_var_decl_with_init(self):
        """Test variable declaration with initialization."""
        stmt = {"type": "VAR_DECL", "name": "y", "init": {"value": 42}}
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 8
        
        assembly_code, updated_offset = handle_var_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )
        
        # Verify offset updated correctly
        self.assertEqual(updated_offset, 12)
        
        # Verify var_offsets updated in-place
        self.assertIn("y", var_offsets)
        self.assertEqual(var_offsets["y"], 8)
        
        # Verify assembly code contains declaration and initialization
        self.assertIn("@ declare variable y at offset 8", assembly_code)
        self.assertIn("MOV r0, #42", assembly_code)
        self.assertIn("STR r0, [sp, #8]", assembly_code)
    
    def test_var_decl_with_zero_init(self):
        """Test variable declaration initialized to zero."""
        stmt = {"type": "VAR_DECL", "name": "z", "init": {"value": 0}}
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 16
        
        assembly_code, updated_offset = handle_var_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )
        
        self.assertEqual(updated_offset, 20)
        self.assertEqual(var_offsets["z"], 16)
        self.assertIn("MOV r0, #0", assembly_code)
        self.assertIn("STR r0, [sp, #16]", assembly_code)
    
    def test_var_decl_with_negative_init(self):
        """Test variable declaration with negative initialization value."""
        stmt = {"type": "VAR_DECL", "name": "neg", "init": {"value": -5}}
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        assembly_code, updated_offset = handle_var_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )
        
        self.assertEqual(updated_offset, 4)
        self.assertEqual(var_offsets["neg"], 0)
        self.assertIn("MOV r0, #-5", assembly_code)
        self.assertIn("STR r0, [sp, #0]", assembly_code)
    
    def test_var_decl_multiple_variables(self):
        """Test multiple variable declarations accumulate in var_offsets."""
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        # First variable
        stmt1 = {"type": "VAR_DECL", "name": "a"}
        assembly1, offset1 = handle_var_decl(
            stmt1, func_name, label_counter, var_offsets, next_offset
        )
        
        # Second variable
        stmt2 = {"type": "VAR_DECL", "name": "b", "init": {"value": 10}}
        assembly2, offset2 = handle_var_decl(
            stmt2, func_name, label_counter, var_offsets, offset1
        )
        
        # Verify both variables in var_offsets
        self.assertIn("a", var_offsets)
        self.assertIn("b", var_offsets)
        self.assertEqual(var_offsets["a"], 0)
        self.assertEqual(var_offsets["b"], 4)
        
        # Verify final offset
        self.assertEqual(offset2, 8)
    
    def test_var_decl_label_counter_unchanged(self):
        """Test that label_counter is not modified by handle_var_decl."""
        stmt = {"type": "VAR_DECL", "name": "x"}
        func_name = "main"
        label_counter: Dict[str, int] = {"while_cond": 1, "if_cond": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        original_counter = label_counter.copy()
        
        handle_var_decl(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Verify label_counter unchanged
        self.assertEqual(label_counter, original_counter)
    
    def test_var_decl_init_none(self):
        """Test variable declaration with init explicitly set to None."""
        stmt = {"type": "VAR_DECL", "name": "w", "init": None}
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        assembly_code, updated_offset = handle_var_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )
        
        self.assertEqual(updated_offset, 4)
        self.assertEqual(var_offsets["w"], 0)
        self.assertNotIn("MOV r0", assembly_code)
        self.assertNotIn("STR r0", assembly_code)
    
    def test_var_decl_with_existing_var_offsets(self):
        """Test variable declaration when var_offsets already has entries."""
        stmt = {"type": "VAR_DECL", "name": "new_var"}
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {"existing": 0, "another": 4}
        next_offset = 8
        
        assembly_code, updated_offset = handle_var_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )
        
        # Verify existing entries preserved
        self.assertEqual(var_offsets["existing"], 0)
        self.assertEqual(var_offsets["another"], 4)
        
        # Verify new variable added
        self.assertEqual(var_offsets["new_var"], 8)
        self.assertEqual(updated_offset, 12)


if __name__ == "__main__":
    unittest.main()
