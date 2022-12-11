import math
import re
from command import Command
#9+3-4/3*34
class Evaluator:
  def __init__(self, stack):
    self._MAXVALUE = 2147483647
    self._MINVALUE = -2147483648
    self._command = Command()
    self._stack = stack
    self._randomNumbers = [1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492,
                     596516649, 1189641421, 1025202362,1350490027, 783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426, 304089172,
                     1303455736, 35005211, 521595368]
    self._randomCounter = 0
    self._precedence = {
      None: 1,  
      '+': 2,
      '-': 2,
      '*': 3,
      '/': 4,
      '%': 5,
      '^': 6
    }

  def numeric_input(self, number):
    """
      Saturates the number and inserts into the stack as a float
    """
    number = self.saturation_check(int(number))
    self._stack.push(float(number))

  def calculate(self, operator):
    """
      Does the calculation by popping the last two values in the stack and applying the operator given. Then pushing back the result to the stack after doing the saturation test.
    """
    try:
      firstDigit = self._stack.pop()  #gets the top of the stack and stores it
      secondDigit = self._stack.pop() #gets the one below the top of the stack and stores it
      if operator == "+": #addition operator
        result = firstDigit + secondDigit
        result = self.saturation_check(result)
        self._stack.push(result)
      elif operator == "-": #subtraction operator
        result = secondDigit - firstDigit
        result = self.saturation_check(result)
        self._stack.push(result)
      elif operator == "*": #multiplication operator
        result = firstDigit * secondDigit
        result = self.saturation_check(result)
        self._stack.push(result)
      elif operator == "/": #division operator
        result = secondDigit / firstDigit
        result = self.saturation_check(result)
        self._stack.push(result)
      elif operator == "%": #modulo operator
        result = secondDigit % firstDigit
        result = self.saturation_check(result)
        self._stack.push(result)
      elif operator == "^": #power operator
        result = math.pow(secondDigit, firstDigit)
        result = self.saturation_check(result)
        self._stack.push(result)
    except Exception as e:
      print(e)

  def saturation_check(self, number):
    """
      Checks if the given number exceeds the minimum value, -2147483648, or maximum value, 2147483647.
      If the number is greater or smaller than MAX or MIN values it will saturate it and returns the number
      :param: number: The number that the wanted to be checked for saturation
      :return: number: The original number or the saturated number (if saturated)
    """
    if number >= self._MAXVALUE:
      number = self._MAXVALUE
    if number <= self._MINVALUE:
      number = self._MINVALUE
    return number

  def operation_check(self, operation):
    """
      By checking the current state of the stack and inputs processed before it decides wheather an operation can be carried on.
      :operation: operation to be checked
      :return: return true if the operation can go ahead
    """
    if self._stack.getLength() < 2:  # Check the stack is big enough to perform an operation
      print("Stack underflow.")
    elif operation == '/' and self._stack.peek() == 0:  # Can't divide by 0
      print("Divide by 0.")
    elif operation == '%' and self._stack.peek() == 0:  # Can't divide by 0
      print("main.sh: line 4:    32 Floating point exception(core dumped) ./srpn/srpn")
      exit(136)
    elif operation == '^' and self._stack.peek() < 0:  # Prints negative power in original
      print("Negative power.")
    else:
      return True

  def empty_stack_handling(self, operator):
    """
       When the stack is empty prints stack empty message when = is entered and minimum value when d is entered.
       :operator: To decide what action to take
       :return: True if the empty stack is handled and False if it isn't handled.
    """
    if self._stack.isEmpty() and operator == '=': #When = is entered and the stack is empty "Stack empty." message displayed
      print("Stack empty.")
      return True
    if self._stack.isEmpty() and operator == 'd': #When d is entered and the stack is empty minimum value,-2147483648, displayed
      print(self._MINVALUE)
      return True
    return False

  def evaluate_operator(self, operator, operator_stack):
    """
      If an operator =, d or r is entered then corresponding operation will be done.
      :operator: To decide what action to take
    """
    if operator == '=':
      if not self.empty_stack_handling(operator): #Prints the top item in the stack after checking the stack is not empty.
        print(int(self._stack.peek()))
    elif operator == 'd':
      if not self.empty_stack_handling(operator): #Dumps the stack if it is not empty
        self._stack.dump()
    elif operator == 'r': #Pushes a random number in to the stack
      if self._randomCounter == 22: #After pushing 22 random numbers it resets to 0 so that it can push the same numbers again.
        self._randomCounter = 0
      self._stack.push(self._randomNumbers[self._randomCounter])
      self._randomCounter += 1
    else:
      if self.operation_check(operator):  #Does the calculation operation after checking there is not going to be any operation issues
        self.calculate(operator)
    

  def evaluate_expression(self, char, operation_stacks, hasNum):
    """
    If it was an expression then based on if it is a infix or postfix expression different evaluations are done. If
    it is infix whenever the numbers are encountered they are pushed on to the stack and when operator is encountered
    they are added to the operator list. When the infix operation ends, determined by the empty character,
    all the operations are evaluated. If it is postfix, all the characters entered will be added to the stack until a
    operator is encountered which then be evaluated.
    :char: character that is seperated by whitespace.
    :operation_stacks: List that contains the operators
    :hasNum: States if there is number in the input
    :returns: counter - how many character got processed, hasNum - stating if number got processed
    """
    counter = 1
    if self.get_num_type(char, hasNum):  #Checks if it is a numeric digit in the form of x, -y, ab..etc
      num = re.search(r'-?\d+', char).group() #Does the regex operation seperate the number in the string literal
      counter = len(num) #Sets the length to the number of the character in the number processed
      self.numeric_input(num) #Puts the number in the stack
      hasNum = True #Sets the hasNum to True as number was encountered.
    elif self.get_expression_type(char): #Checks if it is an expression with infix
      # If there is an operation already in the operators list and it has less precedence then it is evaluated
      if len(operation_stacks) > 0 and not (self._precedence.get(char[0]) >= self._precedence.get(operation_stacks[-1])):
        for operator in reversed(operation_stacks): #Every operators in the reversed operator list, to solve precedence issuem, is evaluated.
          self.evaluate_operator(operator, operation_stacks)
        operation_stacks.clear() #Operation stack is emptied to evaluate the next expression
      operation_stacks.append(char[0]) #The operator is added to the list so that it can be processed next time
      hasNum = False #No number found in the expression as it is an operator
    else:
      print(f"Unrecognised operator or operand \"{char}\".")
    return counter, hasNum

  # Getter functions
  def get_expression_type(self, command):  # Checks if the command is an expression
    if self._command.expression_type(command):
      return True

  def get_num_type(self, command, hasnum):  # Checks if command a numeric digit
    if self._command.num_type(command, hasnum):
      return True

  def get_operator_type(self, command):  # Checks if command is an operator
    if self._command.operator_type(command):
      return True


"""
Three main cases:
1. A number on its own in which case we add it to the stack
2. An invalid character
3. If it is a operator do post fix or infix calculation:
Postfix.....:
Just append in the operator stack
Infix.......:
If there is an number in operator stack and it has low precedence don't do the calculation
"""