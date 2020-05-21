#!/usr/bin/env python

class Node:
    """
    Class for singly linked list node
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    """
    Singly linked list implementation
    """
    def __init__(self):
        self.start_node = None

    def display(self):
        """
        Printing all nodes in list
        """
        if self.start_node == None:
            print("Linked list does not have any items")
            return
        else:
            nodes = []
            curr_node = self.start_node
            while curr_node != None:
                nodes.append(curr_node.data)
                curr_node = curr_node.next
            print(nodes)

    def insert(self, data, pos="end"):
        """
        Insert data into list at different positions
        :param data: data to be inserted
        :param pos: location of the data to be inserted
        """
        node = Node(data)
        if pos == "start":
            if self.start_node == None:
                self.start_node = node
                return
            node.next = self.start_node
            self.start_node = node

        elif pos == "end":
            if self.start_node == None:
                self.start_node = node
                return

            curr_node = self.start_node
            while curr_node.next != None:
                curr_node = curr_node.next
            curr_node.next = node

        else:
            curr_node = self.start_node
            while curr_node != None:
                if curr_node.data == pos:
                    break
                curr_node = curr_node.next
            
            if curr_node == None:
                print("Item not found")
            else:
                node.next = curr_node.next
                curr_node.next = node

    def size(self):
        """
        Returns the size of the list
        """
        if self.start_node == None:
            return 0
        curr_node = self.start_node
        count = 0
        while curr_node != None:
            count += 1
            curr_node = curr_node.next
        return count

    def search_item(self, x):
        if self.start_node == None:
            print(f"{x} not found :(")
            return
        curr_node = self.start_node
        while curr_node != None:
            if curr_node.data == x:
                print(f"{x} found :)")
                return True
            curr_node = curr_node.next
        print(f"{x} not found :(")
        return False

    def delete(self, pos="end"):
        """
        Delete an item from list
        :param pos: location of the data to be inserted
        """
        if pos == "start":
            if self.start_node == None:
                return
            self.start_node = self.start_node.next

        elif pos == "end":
            if self.start_node == None:
                return

            curr_node = self.start_node
            while curr_node.next.next != None:
                curr_node = curr_node.next
            curr_node.next = None

        else:
            if self.start_node == None:
                return
            if self.start_node.data == pos:
                self.start_node = self.start_node.next

            curr_node = self.start_node
            while curr_node.next != None:
                if curr_node.next.data == pos:
                    break
                curr_node = curr_node.next
            curr_node.next = curr_node.next.next

    def reverse(self):
        """
        Display list items in reverse order
        """
        prev = None
        curr_node = self.start_node
        while curr_node != None:
            next_node = curr_node.next
            curr_node.next = prev
            prev = curr_node
            curr_node = next_node
        self.start_node = prev



if __name__ == "__main__":
    linked_list = LinkedList()
    linked_list.insert(20, pos="end")
    linked_list.insert(5, pos="end")
    linked_list.insert(7, pos=20)
    linked_list.insert(9, pos=7)
    linked_list.display()
    linked_list.delete(9)
    linked_list.display()