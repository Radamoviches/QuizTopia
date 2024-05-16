"""
+Class for a Queue data structure using linked lists

+Attributes:
+    head: the first node in the queue
+    last: the last node in the queue
+"""

class Node:
    """
+    Node class for a linked list
+    """

    def __init__(self, data = None):
        """
+        Constructor for the Node class
+        :param data: the data stored in the node
+        """
        self.data = data
        self.next = None


class Queue:
    """
+    Queue class using linked lists
+    """

    def __init__(self):
        """
+        Constructor for the Queue class
+        """
        self.head = None
        self.last = None

    def enqueue(self, data):
        """
+        Enqueue a new item to the end of the queue
+        :param data: the data to be enqueued
+        """
        if not self.last:
            # if the queue is empty, set the new node as both head and last
            self.head = Node(data)
            self.last = self.head
        else:
            # if the queue is not empty, add the new node to the end
            self.last.next = Node(data)
            self.last = self.last.next

    def dequeue(self):
        """
+        Dequeue an item from the front of the queue
+        :return: the data of the dequeued item, or None if the queue is empty
+        """
        if not self.head:
            # return None if the queue is empty
            return None
        val = self.head.data
        self.head = self.head.next
        return val

    def display(self):
        """
+        Print all the items in the queue
+        """
        temp = self.head
        while temp != None:
            print(temp.data)
            temp = temp.next

    def make_empty(self):
        """
+        Clear the queue
+        """
        self.head = None
        self.last = None
