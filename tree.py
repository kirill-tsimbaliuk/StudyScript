from os import system
from abc import ABCMeta, abstractmethod
import sys
import turtle


class Abstract:
    __metaclass__ = ABCMeta

    @abstractmethod
    def call(self):
        pass


class Type(Abstract):
    __metaclass__ = ABCMeta

    @abstractmethod
    def call(self):
        pass


class NoAnswer(Type):

    def __init__(self):
        self.value = None

    def call(self):
        return self.value


class Integer(Type):
    def __init__(self, value):
        self.value = value

    def call(self):
        return int(self.value)


class String(Type):
    def __init__(self, string):
        self.value = string

    def call(self):
        return str(self.value)


class Boolean(Type):
    def __init__(self, value):
        self.value = value

    def call(self):
        return self.value


class BinaryOp(Abstract):
    __metaclass__ = ABCMeta

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def call(self):
        pass


class LogisticOp(Abstract):
    __metaclass__ = ABCMeta

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def call(self):
        pass


class More(LogisticOp):
    def call(self):
        return Boolean(self.left.call() > self.right.call()).call()


class Equals(LogisticOp):
    def call(self):
        return Boolean(self.left.call() == self.right.call()).call()


class Less(LogisticOp):
    def call(self):
        return Boolean(self.left.call() < self.right.call()).call()


class Sum(BinaryOp):
    def call(self):
        try:
            return self.left.call() + self.right.call()
        except TypeError:
            print("Incompatible data type")


class Sub(BinaryOp):
    def call(self):
        try:
            return self.left.call() - self.right.call()
        except TypeError:
            print("Incompatible data type")


class Multiply(BinaryOp):
    def call(self):
        try:
            return self.left.call() * self.right.call()
        except TypeError:
            print("Incompatible data type")


class Div(BinaryOp):
    def call(self):
        try:
            return self.left.call() / self.right.call()
        except TypeError:
            print("Incompatible data type")


class Function(Abstract):
    __metaclass__ = ABCMeta

    def __init__(self, value):
        self.value = value

    @abstractmethod
    def call(self):
        pass


class Print(Function):

    def call(self):
        res = self.value.call()
        if type(res) == bool:
            if res:
                print("true")
            else:
                print("false")
        else:
            print(res)
        return NoAnswer


class Command(Function):

    def call(self):
        system(str(self.value.call()))
        return NoAnswer


class Exit(Function):

    def call(self):
        sys.exit()
