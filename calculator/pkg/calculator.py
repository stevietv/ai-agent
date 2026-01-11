import math

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "**": lambda a, b: a ** b,
            "sqrt": lambda a: math.sqrt(a),
            "%": lambda a: a / 100, # New percentage operator
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 3,
            "sqrt": 4,  # Higher precedence for sqrt
            "%": 4, # Higher precedence for percentage, similar to sqrt
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        # This simple tokenizer assumes space-separated tokens.
        # For more complex expressions, a more robust tokenizer would be needed.
        # Replace percentage sign with space around it to treat it as a separate token
        expression = expression.replace("%", " % ")
        return expression.replace("(", " ( ").replace(")", " ) ").strip().split()

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        i = 0
        while i < len(tokens):\
            token = tokens[i]

            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if operators and operators[-1] == "(":
                    operators.pop()  # Pop the "("
                else:
                    raise ValueError("Mismatched parentheses")
            elif token in self.operators:
                # Handle unary operators like sqrt and %
                if token == "sqrt" or token == "%":
                    operators.append(token)
                else:
                    while (
                        operators
                        and operators[-1] in self.operators
                        and self.precedence.get(operators[-1], 0) >= self.precedence[token]
                    ):
                        self._apply_operator(operators, values)
                    operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")
            i += 1

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()

        if operator == "sqrt" or operator == "%": # Handle unary sqrt and %
            if len(values) < 1:
                raise ValueError(f"not enough operands for operator {operator}")
            a = values.pop()
            values.append(self.operators[operator](a))
        else:
            if len(values) < 2:
                raise ValueError(f"not enough operands for operator {operator}")
            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))\n