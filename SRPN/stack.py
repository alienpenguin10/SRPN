class Stack:

  def __init__(self):
    """
      Initialises a stack with size 23
    """
    self._length = 23
    self._StackArray = ['\0'] * 23
    self._top = -1

  def isFull(self):
    """
      Checks the length of the stack reached its maximum
    """
    if (self._top == self._length - 1):
      return True
    else:
      return False

  def isEmpty(self):
    """
      Checks if there is no element in the stack
    """
    if (self._top == -1):
      return True
    else:
      return False

  def peek(self):
    """
      Gets the top element in the array
    """
    return (self._StackArray[self._top])

  def peekMore(self, index):
    """
      Returns the element in the given index
    """
    return (self._StackArray[self._top - (index - 1)])

  def pop(self):
    """
      Removes and returns the top element in the array
    """
    self._top -= 1
    popedValue = self._StackArray[self._top + 1]
    self._StackArray[self._top + 1] = '\0'
    return popedValue

  def getLength(self):
    """
        Gets the length of the array
    """
    counter = 0
    for item in self._StackArray:
      if item != '\0':
        counter += 1
    return counter

  def push(self, number):
    """
        Push the given element in to the array
    """
    if (self.isFull() == True):
      print("Stack overflow.")
    else:
      self._top += 1
      self._StackArray[self._top] = number

  def dump(self):
    """
        Prints the entire stack
    """
    for item in self._StackArray:
      if item != '\0':
        print(int(item))
