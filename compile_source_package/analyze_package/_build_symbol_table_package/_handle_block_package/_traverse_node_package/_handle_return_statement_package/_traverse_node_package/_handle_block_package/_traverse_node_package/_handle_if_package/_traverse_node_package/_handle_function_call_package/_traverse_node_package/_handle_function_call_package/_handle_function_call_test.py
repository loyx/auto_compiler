# -*- coding: utf-8 -*-
"""Unit tests for _handle_function_call function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._handle_function_call_src import _handle_function_call

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]