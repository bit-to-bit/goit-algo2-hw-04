class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def put(self, key, value=None):
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for put: key = {key} must be a non-empty string")
        current = self.root
        for char in key:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        if current.value is None:
            self.size += 1
        current.value = value

    def get(self, key):
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for get: key = {key} must be a non-empty string")
        current = self.root
        for char in key:
            if char not in current.children:
                return None
            current = current.children[char]
        return current.value

    def contains(self, key):
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for contains: key = {key} must be a non-empty string")
        return self.get(key) is not None

    def keys_with_prefix(self, prefix):
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument for keys_with_prefix: prefix = {prefix} must be a string")
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        result = []
        self._collect(current, list(prefix), result)
        return result

    def _collect(self, node, path, result):
        if node.value is not None:
            result.append("".join(path))
        for char, next_node in node.children.items():
            path.append(char)
            self._collect(next_node, path, result)
            path.pop()

    def keys(self):
        result = []
        self._collect(self.root, [], result)
        return result
