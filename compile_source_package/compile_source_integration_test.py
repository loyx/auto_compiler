#!/usr/bin/env python3
"""Integration tests for compile_source function."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from compile_source_package.compile_source_src import compile_source


class TestCompileSourceIntegration(unittest.TestCase):
    """Integration tests for compile_source covering real module boundaries."""

    def _create_temp_source(self, content: str):
        """Helper to create a temporary source file."""
        fd, path = tempfile.mkstemp(suffix=".c")
        try:
            os.write(fd, content.encode("utf-8"))
            os.close(fd)
            yield path
        finally:
            os.unlink(path)

    def test_compile_hello_world(self):
        """Test compiling a complete minimal C program."""
        source_code = """
int main() {
    return 0;
}
"""
        with self._create_temp_source(source_code) as source_file:
            config = {"source_file": source_file}
            assembly = compile_source(config)

            self.assertIsInstance(assembly, str)
            self.assertTrue(len(assembly) > 0)
            self.assertIn("main", assembly)

    def test_compile_with_variables(self):
        """Test compiling code with variable declarations and operations."""
        source_code = """
int main() {
    int x = 42;
    int y = x + 1;
    return y;
}
"""
        with self._create_temp_source(source_code) as source_file:
            config = {"source_file": source_file}
            assembly = compile_source(config)

            self.assertIsInstance(assembly, str)
            self.assertTrue(len(assembly) > 0)

    def test_compile_with_control_flow(self):
        """Test compiling code with while loop."""
        source_code = """
int main() {
    int i = 0;
    while (i < 10) {
        i = i + 1;
    }
    return i;
}
"""
        with self._create_temp_source(source_code) as source_file:
            config = {"source_file": source_file}
            assembly = compile_source(config)

            self.assertIsInstance(assembly, str)
            self.assertTrue(len(assembly) > 0)

    def test_compile_with_function_call(self):
        """Test compiling code with function definitions and calls."""
        source_code = """
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(1, 2);
    return result;
}
"""
        with self._create_temp_source(source_code) as source_file:
            config = {"source_file": source_file}
            assembly = compile_source(config)

            self.assertIsInstance(assembly, str)
            self.assertTrue(len(assembly) > 0)
            self.assertIn("add", assembly)
            self.assertIn("main", assembly)

    def test_file_not_found(self):
        """Test error handling when source file doesn't exist."""
        config = {"source_file": "/nonexistent/path/source.c"}

        with self.assertRaises(FileNotFoundError):
            compile_source(config)

    def test_compile_with_if_statement(self):
        """Test compiling code with if-else control flow."""
        source_code = """
int main() {
    int x = 5;
    if (x > 0) {
        return 1;
    } else {
        return 0;
    }
}
"""
        with self._create_temp_source(source_code) as source_file:
            config = {"source_file": source_file}
            assembly = compile_source(config)

            self.assertIsInstance(assembly, str)
            self.assertTrue(len(assembly) > 0)


if __name__ == "__main__":
    unittest.main()
