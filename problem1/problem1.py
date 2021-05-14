# Joining path in order to import modules from other exercises/problems
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# Importing the LinkedList class from problem5
from problem5.problem5 import LinkedList


class Stack:
    def __init__(self):
        self.stack = LinkedList()

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack.get(-1)
    
    def is_empty(self):
        return len(self.stack) == 0
    
def main():
    stack = Stack()
    stack.push('Introductory App Dev Concepts')
    stack.push('Intermediate App Dev Concepts')
    stack.push('Advanced App Dev Concepts')
    
    stack.pop()

    print(f'{stack.peek()} is at the top of the stack')

    while not stack.is_empty():
        print("The stack is not empty")
        stack.pop()

if __name__ == '__main__':
    main()

