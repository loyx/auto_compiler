# Re-export _traverse_node for patching in tests
from .._traverse_node_src import _traverse_node

__all__ = ["_traverse_node"]
