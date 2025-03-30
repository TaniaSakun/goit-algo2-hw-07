class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Inserts a new node into the tree."""
        if not self.root:
            self.root = Node(key, value)
        else:
            node = self._insert_node(key, value, self.root)
            self._splay(node)

    def _insert_node(self, key, value, current_node):
        """Iteratively inserts node into the tree."""
        parent = None
        while current_node:
            parent = current_node
            if key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node = Node(key, value, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        return new_node

    def find(self, key):
        """Finds a node with the given key."""
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node.value
        return None

    def _splay(self, node):
        """Splays node to the root of tree."""
        while node.parent:
            if node.parent.parent is None:  # Zig case
                self._rotate(node)
            elif node == node.parent.left and node.parent == node.parent.parent.left:  # Zig-Zig case
                self._rotate(node.parent)
                self._rotate(node)
            elif node == node.parent.right and node.parent == node.parent.parent.right:  # Zig-Zig case
                self._rotate(node.parent)
                self._rotate(node)
            else:  # Zig-Zag case
                self._rotate(node)
                self._rotate(node)

    def _rotate(self, node):
        """Rotates the node to the root."""
        parent = node.parent
        grandparent = parent.parent
        is_left_child = (parent.left == node)
        
        # Rotate the node to the root
        if is_left_child:
            self._rotate_right(parent)
        else:
            self._rotate_left(parent)
        
        if grandparent is None:
            self.root = node
        else:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        
        # Rotate the node to root if necessary
        if grandparent:
            self._rotate(node)

    def _rotate_right(self, node):
        """Rotates the node to the right side."""
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child
        
        left_child.right = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Rotates the node to the left side."""
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        
        right_child.left = node
        node.parent = right_child