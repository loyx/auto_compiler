# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expr_package._parse_or_expr_src import _parse_or_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (NUMBER, STRING, IDENTIFIER, OPERATOR, etc.)
#   "value": str,            # token 值 (原始字符串)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, LITERAL, IDENTIFIER, CALL, etc.)
#   "left": AST,             # 左操作数 (BINARY_OP)
#   "right": AST,            # 右操作数 (BINARY_OP)
#   "operator": str,         # 运算符字符串
#   "operand": AST,          # 操作数 (UNARY_OP)
#   "value": Any,            # 字面量值
#   "literal_type": str,     # 字面量类型 (NUMBER, STRING, BOOL, NONE)
#   "name": str,             # 标识符名称
#   "callee": AST,           # 被调用函数 (CALL)
#   "arguments": list,       # 参数列表 (CALL)
#   "elements": list,        # 列表元素 (LIST)
#   "entries": list,         # 字典键值对 (DICT)
#   "object": AST,           # 对象 (ATTRIBUTE, SUBSCRIPT)
#   "attribute": str,        # 属性名 (ATTRIBUTE)
#   "index": AST,            # 索引 (SUBSCRIPT)
#   "condition": AST,        # 条件 (TERNARY)
#   "if_true": AST,          # 真值分支 (TERNARY)
#   "if_false": AST,         # 假值分支 (TERNARY)
#   "children": list,        # 子节点列表
#   "message": str,          # 错误消息 (ERROR)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析完整表达式（包含运算符优先级）。
    输入：parser_state（解析器状态）
    输出：表达式的 AST 节点
    副作用：更新 parser_state['pos'] 越过已解析的 token
    """
    # 从最低优先级开始解析，逐层上升到最高优先级
    # expression → or_expr → and_expr → comparison → term → factor → unary → primary
    return _parse_or_expr(parser_state)

# === helper functions ===
# 表达式解析采用递归下降，各优先级层次已委托给子函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是纯函数式解析器模块
