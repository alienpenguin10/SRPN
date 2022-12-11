from stack import Stack
from evaluator import Evaluator
import math
import re

#Stored as float and value is floored
#Constants:
commentMode = False

def setup_srpn():
  """
  Sets up the variables, objects and values needed for the srpn to function.
      :return: Stack, stack_operators, evaluator.
  """
  stack = Stack() #Stack object that represents the stack where the values will be stored
  evaluator = Evaluator(stack) #Evaluator object that evaluates and process the calculations
  stack_operators = [] #list to store the operators entered by the user in the order they appear in the input
  return stack, stack_operators, evaluator

def process_char(char, stack, stack_operators, hasNum, evaluator):
  """
  Processes the individual block of character(s) that are seperated by the whitespace and passes it to the write function depending on the type.
      :param char: The character that is inputted by the user.
      :param stack_operators: List of operators that the user has currently entered.
      :param hasNum: A boolean variable that tells there is a numeric value in the input.
      :param evaluator: Evaluator object that process the input and does the calculations
      :return: Recursive function calls itself until the length of the character becomes 0.
  """
  if len(char) == 0: #Checks if the char is empty (with no chars left) which is the base case for the recursion
    if not (len(stack_operators) == 0): #If there are any opertors left in the list
      for operator in reversed(stack_operators): # iterate over list in reverse order because of the precedence issue
        evaluator.evaluate_operator(operator, stack_operators) #evaluates the remaining operators to do the calculations
      stack_operators.clear() #Clears operator list to do the next set of calculations
    return
  if evaluator.get_expression_type(char): #If the input is an expression. i.e. a+b, x, -y, +, -
    counter, hasNum = evaluator.evaluate_expression(char,stack_operators, hasNum)
  elif evaluator.get_operator_type(char[0]): #Operators such as =, d, r, +, -...etc in its own
    hasNum = False
    evaluator.evaluate_operator(char[0], stack_operators)
    counter = 1
  else:#Unrecognised operator is entered
    print(f"Unrecognised operator or operand \"{char[0]}\".")
    counter = 1
  process_char(char[counter:], stack, stack_operators, hasNum, evaluator) #Recursivly calls the function


def process_command(command, stack, stack_operators, evaluator):
  """
  Processes the input that are seperated by the line and decides whether it has to activate comment mode or not. Calls the process_char method to process the input seperated by the spaces.
      :param command: The entire line that is inputted by the user.
      :param stack_operators: Newly created stack_operators
      :param hasNum: A boolean variable that tells there is a numeric value in the input.
      :param evaluator: Evaluator object that process the input and does the calculations
  """
  global commentMode
  for i in command.split():  # Split the command by white space
    hasNum = False
    if i == '#':
      # Decides if the comment mode has to be activated or deactivated
      if commentMode == False: #if it is not already in comment mode it turns it turns on
        commentMode = True
      else: #if it is not in comment mode it turns off
        commentMode = False
    elif not commentMode:
      process_char(i, stack, stack_operators, hasNum, evaluator) #Otherwise just process the entered input


#This is the entry point for the program.
#It is suggested that you do not edit the below,
#to ensure your code runs with the marking script
if __name__ == "__main__":
  stack, stack_operators, evaluator = setup_srpn() #calls the setup function the initialise the srpn
  while True:
    try:
      cmd = input()
      pc = process_command(cmd, stack, stack_operators, evaluator)
    except EOFError:
      exit()
