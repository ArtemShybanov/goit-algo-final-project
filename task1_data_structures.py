class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Previous node does not exist.")
            return

        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head

        if cur and cur.data == key:
            self.head = cur.next
            return

        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next

        if cur is None:
            return

        prev.next = cur.next

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    # Reverse linked list
    def reverse(self):
        prev = None
        cur = self.head

        while cur:
            nxt = cur.next # Save next node
            cur.next = prev # Reverse pointer
            prev = cur # Move prev forward
            cur = nxt # Move cur forward

        self.head = prev # New head is the old tail

    # Sort linked list (merge sort)
    def merge_sort(self):
        self.head = self._merge_sort_head(self.head)

    def _merge_sort_head(self, head: Node | None) -> Node | None:
        # Base case: empty list or single node list is already sorted
        if head is None or head.next is None:
            return head

        # Split the list into two halves
        left, right = self._split_in_half(head)

        # Recursively sort both halves
        left_sorted = self._merge_sort_head(left)
        right_sorted = self._merge_sort_head(right)

        # Merge the two sorted halves
        return self._merge_two_sorted_heads(left_sorted, right_sorted)

    def _split_in_half(self, head: Node) -> tuple[Node, Node]:
        # Use slow/fast pointers to find the middle
        slow = head
        fast = head
        prev = None

        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        # Cut the list into two parts
        prev.next = None
        return head, slow

    def _merge_two_sorted_heads(self, a: Node | None, b: Node | None) -> Node | None:
        dummy = Node(0)
        tail = dummy

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        # Attach the remaining part
        tail.next = a if a else b
        return dummy.next

    # Merge two sorted linked lists into one sorted list
    @staticmethod
    def merge_sorted_lists(list_a: "LinkedList", list_b: "LinkedList") -> "LinkedList":
        merged = LinkedList()
        merged.head = merged._merge_two_sorted_heads(list_a.head, list_b.head)
        return merged


# Test case
llist = LinkedList()

# Insert nodes at the beginning
llist.insert_at_beginning(5)
llist.insert_at_beginning(10)
llist.insert_at_beginning(15)

# Insert nodes at the end
llist.insert_at_end(20)
llist.insert_at_end(25)

print("Linked list:")
llist.print_list()

# Reverse
llist.reverse()
print("\nReversed linked list:")
llist.print_list()

# Sort (merge sort)
llist.merge_sort()
print("\nSorted linked list:")
llist.print_list()

# Create two sorted lists and merge them
a = LinkedList()
for x in [1, 4, 7, 10]:
    a.insert_at_end(x)

b = LinkedList()
for x in [2, 3, 8, 9, 11]:
    b.insert_at_end(x)

merged = LinkedList.merge_sorted_lists(a, b)
print("\nMerged sorted lists (A + B):")
merged.print_list()