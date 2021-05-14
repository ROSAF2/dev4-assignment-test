class Node:
    def __init__(self,data = None):
        self.data = data
        self.next = None

class LinkedListIterator:
    def __init__(self,ll):
        self.ll = ll
        self.next_index = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.ll.get(self.next_index)
            self.next_index += 1
            return result 
        except IndexError:
            raise StopIteration

class LinkedList:
    def __init__(self):
        self.head = Node()

    def append(self,data):
        new_node = Node(data)
        if self.head.data is None: # If head is empty
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next: # While current_node.next is not null
                current_node = current_node.next
            current_node.next = new_node # Add reference of new node to last node
    
    def pop(self):
        # Evaluate head node
        if self.head.next is None: # If head has no next reference
            if self.head.data is None: # If no data
                raise IndexError("Trying to pop from empty linked list")   
            else: # if head has data
                data = self.head.data
                self.head.data = None # Deletes data
                return data
        else: # if head has data and reference
            previous_node = Node() # Null node
            current_node = self.head
            while current_node.next: # While current_node.next is not null
                previous_node = current_node
                current_node = current_node.next
            previous_node.next = None 
            return current_node.data

    def get(self,index):
        """ Gets the node data in the list with the provided index """
        if index >= 0: # Positive Index
            if index >= len(self):
                raise IndexError('Index out of bounds')
            current_index = 0
            current_node = self.head
            while True:
                if current_index == index: return current_node.data
                current_node = current_node.next
                current_index += 1
            
        else: #Negative Index
            if abs(index) > len(self):
                raise IndexError('Index out of bounds')
            current_index = -1 * len(self)
            current_node = self.head
            while True:
                if current_index == index: return current_node.data
                current_node = current_node.next
                current_index += 1

    def __len__(self):
        count = 0
        # Evaluate head
        if self.head.next is None:
            if self.head.data is None: return count
            else:
                count += 1
                return count
        else: # if head has data and reference
            count += 1
            current_node = self.head
            while current_node.next: # While current_node.next is not null
                current_node = current_node.next
                count += 1
            return count
    
    def __iter__(self):
        return LinkedListIterator(self)
    
def main():

    ll = LinkedList()

    # implement an append method
    print('The first 7 even numbers will be appended to the list\n')
    for i in range(1,8):
        ll.append(2*i)

    # implement a pop method
    print('The last 4 elements will be poped from the list')
    for i in range(4):
        print(f'Element: {ll.pop()} is now gone')

    # report its length when queried with the len() function.

    print(f'\nThe length of the linked list is: {len(ll)}\n')

    # implement the Iterator pattern so it can be used in a for loop.
    print('Looping through the list we get:')
    for item in ll:
        print(item, end=' ')

if __name__ == '__main__':
    main()
