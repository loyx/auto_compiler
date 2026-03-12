#!/usr/bin/env python3
"""Integration tests for handle_var_decl function."""

import sys
import os

# Add project root to path
# Current file is in: handle_var_decl_package/
# Need to go up 5 levels to reach project root where generate_function_code_package exists
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

from handle_var_decl_package.handle_var_decl_src import (
    handle_var_decl,
)
from handle_var_decl_package.generate_expression_code_package.generate_expression_code_src import (
    generate_expression_code,
)