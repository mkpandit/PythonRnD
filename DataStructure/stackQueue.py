#!/usr/bin/env python

class Stack:
    """
    Implementing Stack using built-in list
    Stack follows LIFO
    """
    def __init__(self):
        self.stack = []

    def __str__(self):
        items = ", ".join(self.stack)
        return f"Items in Stack: {items}"

    def pop(self):
        if len(self.stack) < 1:
            return None
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def size(self):
        return len(self.stack)

class Queue:
    """
    Implementing Queue using built-in list
    Queue follows FIFO
    """
    def __init__(self):
        self.queue = []

    def __str__(self):
        items = ", ".join(self.queue)
        return f"Items in Queue: {items}"

    def pop(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    def push(self, item):
        self.queue.append(item)

    def size(self):
        return len(self.queue)

if __name__ == '__main__':
    stack = Stack()
    stack.push("Here")
    stack.push("There")
    stack.push("007")
    print(stack)
    stack.pop()
    print(stack)

    queue = Queue()
    queue.push("Here")
    queue.push("There")
    queue.push("007")
    print(queue)
    queue.pop()
    print(queue)