"""
Calculator tool implementation.
"""
import ast
import operator
import math
from typing import Optional, Any, Dict
from agents.tool import function_tool

from .base import BaseTool
from ..config.logging import get_logger

logger = get_logger(__name__)


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
    
    def _eval(self, node: ast.AST) -> Any:
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


class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations."""
    
    def __init__(self):
        super().__init__(
            name="calculate",
            description="Perform mathematical calculations including basic arithmetic, functions, and scientific operations"
        )
        self.evaluator = SafeMathEvaluator()
    
    async def execute(self, expression: str) -> str:
        """
        Execute a mathematical calculation.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Calculation result as a string
        """
        logger.info("Calculating expression", expression=expression)
        
        try:
            result = self.evaluator.evaluate(expression)
            
            # Format the result nicely
            if isinstance(result, float):
                if result.is_integer():
                    formatted_result = str(int(result))
                else:
                    formatted_result = f"{result:.10g}"  # Remove trailing zeros
            else:
                formatted_result = str(result)
            
            response = f"{expression} = {formatted_result}"
            logger.info("Calculation completed", expression=expression, result=formatted_result)
            return response
            
        except Exception as e:
            error_msg = f"Error calculating '{expression}': {str(e)}"
            logger.error("Calculation failed", expression=expression, error=str(e))
            return error_msg
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for calculator tool parameters"""
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5', 'sqrt(16)')"
                }
            },
            "required": ["expression"]
        }
    
    def get_function_tool(self):
        """Return the function_tool decorated version."""
        
        @function_tool
        def calculate(expression: str) -> str:
            """
            Perform mathematical calculations.
            
            Args:
                expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4", "sqrt(16)", "sin(pi/2)")
                
            Returns:
                Calculation result as a string
                
            Examples:
                - Basic arithmetic: "2 + 3 * 4" → "2 + 3 * 4 = 14"
                - Functions: "sqrt(16)" → "sqrt(16) = 4"
                - Scientific: "sin(pi/2)" → "sin(pi/2) = 1"
            """
            logger.info("Calculating expression via function tool", expression=expression)
            
            try:
                result = self.evaluator.evaluate(expression)
                
                # Format the result nicely
                if isinstance(result, float):
                    if result.is_integer():
                        formatted_result = str(int(result))
                    else:
                        formatted_result = f"{result:.10g}"  # Remove trailing zeros
                else:
                    formatted_result = str(result)
                
                response = f"{expression} = {formatted_result}"
                logger.info("Calculation completed via function tool", expression=expression, result=formatted_result)
                return response
                
            except Exception as e:
                error_msg = f"Error calculating '{expression}': {str(e)}"
                logger.error("Calculation failed via function tool", expression=expression, error=str(e))
                return error_msg
        
        return calculate


# Create global instance
calculator_tool = CalculatorTool()