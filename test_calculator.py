#!/usr/bin/env python3
"""
Test script to verify calculator tool functionality.
"""
import ast
import operator
import math


class SafeMathEvaluator:
    """Safe mathematical expression evaluator."""
    
    # Allowed operators
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    # Allowed functions
    functions = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'ceil': math.ceil,
        'floor': math.floor,
        'pi': math.pi,
        'e': math.e,
    }
    
    def evaluate(self, expression: str) -> float:
        """Safely evaluate a mathematical expression."""
        try:
            # Parse the expression
            node = ast.parse(expression.strip(), mode='eval')
            return self._eval(node.body)
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _eval(self, node: ast.AST):
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
            return node.n
        elif isinstance(node, ast.Name):
            if node.id in self.functions:
                return self.functions[node.id]
            else:
                raise ValueError(f"Unknown variable: {node.id}")
        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op(operand)
        elif isinstance(node, ast.Call):
            func = self._eval(node.func)
            if not callable(func):
                raise ValueError(f"Not a function: {func}")
            args = [self._eval(arg) for arg in node.args]
            return func(*args)
        elif isinstance(node, ast.List):
            return [self._eval(item) for item in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(self._eval(item) for item in node.elts)
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")


def test_calculator():
    """Test the calculator functionality."""
    print("🧮 Testing Calculator Logic")
    print("=" * 50)
    
    evaluator = SafeMathEvaluator()
    
    test_cases = [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("6 * 7", 42),
        ("15 / 3", 5),
        ("2 ** 3", 8),
        ("sqrt(16)", 4),
        ("sqrt(144)", 12),
        ("2 ** 3 + sqrt(16) * 5", 28),  # 8 + 4*5 = 28
        ("sin(pi/2)", 1),
        ("cos(0)", 1),
        ("log10(100)", 2),
        ("max(5, 10, 3)", 10),
        ("min(5, 10, 3)", 3),
        ("abs(-42)", 42),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for expression, expected in test_cases:
        try:
            result = evaluator.evaluate(expression)
            if abs(result - expected) < 1e-10:  # Handle floating point precision
                print(f"✅ {expression} = {result}")
                passed += 1
            else:
                print(f"❌ {expression} = {result} (expected {expected})")
        except Exception as e:
            print(f"❌ Error with '{expression}': {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    print("\n🔍 Testing Error Handling")
    print("=" * 50)
    
    error_cases = [
        "invalid_function(5)",
        "2 +",
        "/ 5",
        "unknown_var",
    ]
    
    for expression in error_cases:
        try:
            result = evaluator.evaluate(expression)
            print(f"❌ Expected error with '{expression}' but got: {result}")
        except Exception as e:
            print(f"✅ Correctly caught error with '{expression}': {type(e).__name__}")


if __name__ == "__main__":
    test_calculator()
