class Command:
  """
      Will return true if one of the following meets:
      1. If the first character is numeric
      2. If there is more than one character available and it has as '-' and its on its own
  """
  def num_type(self, char, hasNum):
    if (char[0].isnumeric()) or (len(char) > 1 and char[0] == '-' and char[1].isnumeric() and not hasNum):
      return True

  """
    Will return true if one of the following meets if it is part of infix expression
  """
  def expression_type(self, char):
    #if it is a - number or negative integer or containing operator
    if (char[0].isnumeric() or (len(char) > 1 and char[0] == '-' and char[1].isnumeric())) or (char[0] in ['+', '-', "*", "/", "%", "^"]):
      return True

  def operator_type(self, char):
    if char in ['+', '-', "*", "/", "%", "^", "=", "d", "r"]:
      return True

#Type to be determined:
"""
Types(T):
1.Single positive or negative integer. (C1)i.e. x, -y..etc
2.Part of an expression: number(C1) or contain expresion operator (C3). i.e. +34=
3.Just only an operator (C2)
"""
#Checks to be done:
"""
Checks(C):
1. If it is a number - positive or negative
2. Operator - +, *, / ...etc
3. Expression operator - operator within the expression
4. Valid input - is number or operator
"""