# Joining path in order to import modules from other exercises/problems
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 

# Importing the Stack class from problem1
from problem1.problem1 import Stack


class Addition:
    def add(self, num1,num2):
        return num1 + num2

class Multiplication:
    def multiply(self, num1,num2):
        return num1 * num2
    
class Substraction:
    def substract(self, num1,num2):
        return num1 - num2

class Division:
    def divide(self, num1,num2):
        return num1 / num2

from enum import Enum
class Operators(Enum):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    OVER = '/'

class CalculationFactory:
    @staticmethod
    def calculate(num1,operator,num2):
        if operator == '+':
            return Addition().add(num1,num2)
        elif operator == '*':
            return Multiplication().multiply(num1,num2)
        elif operator == '-':
            return Substraction().substract(num1,num2)
        elif operator == '/':
            return Division().divide(num1,num2)

def calculatePostfixExpression(splitExpression):
    stack = Stack()

    for i in splitExpression:
        try:
            stack.push(int(i)) # cast string element to int
        except ValueError:
            operators = [ i.value for i in Operators ] # Enum values
            if i in operators:
                operand2 = stack.pop()
                operand1 = stack.pop()

                result = CalculationFactory.calculate(operand1,i,operand2)
                stack.push(result)

            else: 
                raise ValueError(i)
    return int(stack.pop())


def main():
    expression = input('Enter postfix expression: ')
    # expression ='46 8 4 * 2 / +' 
    splitExpression = expression.split(' ')

    result = calculatePostfixExpression(splitExpression)
    print(result)
    
if __name__ == '__main__':
    main()