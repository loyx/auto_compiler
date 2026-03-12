# === std / third-party imports ===

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expr_package._parse_expr_src import _parse_expr
from ._parse_block_package._parse_block_src import _parse_block

# === ADT defines ===
# 无需重新定义 Token/AST/ParserState，使用 dict 类型注解
# 参考上级共享上下文中的类型定义：
# Token = Dict[str, Any]
# AST = Dict[str, Any]
# ParserState = Dict[str, Any]

# === main function ===
def _parse_if_stmt(parser_state: dict) -> dict:
    """
    解析 if 语句，返回 IF 类型 AST 节点。
    
    语法格式：if (表达式) 语句块 [else 语句块]
    输入：parser_state（pos 指向 IF token）
    输出：IF AST 节点，结构为：
        {
            "type": "IF",
            "children": [condition_ast, then_block_ast, else_block_ast],
            "line": int,
            "column": int
        }
    """
    # 消费 IF token 并记录位置
    if_token = _consume_token(parser_state, "IF")
    line = if_token["line"]
    column = if_token["column"]
    
    # 消费 LPAREN（左圆括号）
    _consume_token(parser_state, "LPAREN")
    
    # 解析条件表达式
    condition_ast = _parse_expr(parser_state)
    
    # 消费 RPAREN（右圆括号）
    _consume_token(parser_state, "RPAREN")
    
    # 解析 then 语句块
    then_block_ast = _parse_block(parser_state)
    
    # 检查是否有 ELSE token
    else_block_ast = None
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        _consume_token(parser_state, "ELSE")
        else_block_ast = _parse_block(parser_state)
    
    # 构建并返回 IF AST 节点
    return {
        "type": "IF",
        "children": [condition_ast, then_block_ast, else_block_ast],
        "line": line,
        "column": column
    }

# === helper functions ===
# 无 helper 函数，逻辑已在 main 函数中完成

# === OOP compatibility layer ===
# 无需 OOP wrapper，此为普通函数节点