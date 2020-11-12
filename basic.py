from doggoscript.lexer import *
from doggoscript.parser import *
from doggoscript import Context, SymbolTable
from doggoscript.interpreter import *

from easy_getch import getch

import string, os, math, random

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("pi", Number.pi)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("print_ret", BuiltInFunction.print_ret)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_num", BuiltInFunction.is_number)
global_symbol_table.set("is_str", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_fun", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("sqrt", BuiltInFunction.sqrt)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("lower", BuiltInFunction.lower)
global_symbol_table.set("random", BuiltInFunction.random)
global_symbol_table.set("print_end", BuiltInFunction.print_end)
global_symbol_table.set("input_prompt", BuiltInFunction.input_prompt)
global_symbol_table.set("getch", BuiltInFunction.getch)
global_symbol_table.set("py_eval", BuiltInFunction.py_eval)
global_symbol_table.set("ord", BuiltInFunction.ord)
global_symbol_table.set("bin", BuiltInFunction.bin)
global_symbol_table.set("doggoiscute", BuiltInFunction.doggoiscute)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    print(f"Tokens: {tokens}")

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
