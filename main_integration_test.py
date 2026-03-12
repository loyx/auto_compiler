#!/usr/bin/env python3
"""
Integration tests for main function.
Tests the orchestration flow of the C to ARM64 assembly compiler.
"""

import sys
import io
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main_package.main_src import main


class TestMainIntegration:
    """Integration tests for the main entrypoint function."""

    def test_main_success_stdout(self):
        """Test successful compilation with output to stdout."""
        mock_config = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": False
        }
        mock_assembly = "    mov x0, #0\n    ret\n"

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', return_value=mock_assembly):
                captured = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = captured
                try:
                    result = main()
                finally:
                    sys.stdout = old_stdout

                assert result == 0
                assert captured.getvalue().strip() == mock_assembly.strip()

    def test_main_success_file_output(self):
        """Test successful compilation with output to file."""
        mock_config = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": False
        }
        mock_assembly = "    mov x0, #0\n    ret\n"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.s') as tmp:
            tmp_path = tmp.name

        try:
            mock_config["output_file"] = tmp_path

            with patch('main_package.main_src.parse_arguments', return_value=mock_config):
                with patch('main_package.main_src.compile_source', return_value=mock_assembly):
                    result = main()

                    assert result == 0
                    with open(tmp_path, 'r') as f:
                        content = f.read()
                    assert content == mock_assembly
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_main_file_not_found(self):
        """Test FileNotFoundError handling."""
        mock_config = {
            "source_file": "nonexistent.c",
            "output_file": None,
            "verbose": False
        }

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', side_effect=FileNotFoundError("source file not found")):
                captured = io.StringIO()
                old_stderr = sys.stderr
                sys.stderr = captured
                try:
                    result = main()
                finally:
                    sys.stderr = old_stderr

                assert result == 1
                assert "error:" in captured.getvalue()

    def test_main_general_exception(self):
        """Test general exception handling."""
        mock_config = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": False
        }

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', side_effect=Exception("compilation failed")):
                captured = io.StringIO()
                old_stderr = sys.stderr
                sys.stderr = captured
                try:
                    result = main()
                finally:
                    sys.stderr = old_stderr

                assert result == 1
                assert "error:" in captured.getvalue()

    def test_main_compile_exception(self):
        """Test compilation-specific exception handling."""
        mock_config = {
            "source_file": "invalid.c",
            "output_file": None,
            "verbose": False
        }

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', side_effect=ValueError("syntax error at line 5")):
                captured = io.StringIO()
                old_stderr = sys.stderr
                sys.stderr = captured
                try:
                    result = main()
                finally:
                    sys.stderr = old_stderr

                assert result == 1
                assert "error:" in captured.getvalue()

    def test_main_file_write_exception(self):
        """Test file write exception handling."""
        mock_config = {
            "source_file": "test.c",
            "output_file": "/nonexistent/path/output.s",
            "verbose": False
        }
        mock_assembly = "    mov x0, #0\n    ret\n"

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', return_value=mock_assembly):
                captured = io.StringIO()
                old_stderr = sys.stderr
                sys.stderr = captured
                try:
                    result = main()
                finally:
                    sys.stderr = old_stderr

                assert result == 1
                assert "error:" in captured.getvalue()

    def test_main_empty_assembly(self):
        """Test edge case: empty assembly output."""
        mock_config = {
            "source_file": "empty.c",
            "output_file": None,
            "verbose": False
        }
        mock_assembly = ""

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', return_value=mock_assembly):
                captured = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = captured
                try:
                    result = main()
                finally:
                    sys.stdout = old_stdout

                assert result == 0
                assert captured.getvalue() == "\n"

    def test_main_verbose_config(self):
        """Test that verbose config is passed through correctly."""
        mock_config = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": True
        }
        mock_assembly = "    mov x0, #0\n    ret\n"

        with patch('main_package.main_src.parse_arguments', return_value=mock_config):
            with patch('main_package.main_src.compile_source', return_value=mock_assembly):
                captured = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = captured
                try:
                    result = main()
                finally:
                    sys.stdout = old_stdout

                assert result == 0
                assert mock_config["verbose"] is True


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
