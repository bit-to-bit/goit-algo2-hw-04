from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError(f"Illegal argument: pattern = {pattern} must be a string")
        if not pattern:
            raise ValueError("Illegal argument: pattern must be a non-empty string")
        words = self.keys()
        return sum(1 for word in words if word.endswith(pattern))

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument: prefix = {prefix} must be a string")
        if not prefix:
            raise ValueError("Illegal argument: prefix must be a non-empty string")
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    assert trie.count_words_with_suffix("e") == 1
    assert trie.count_words_with_suffix("ion") == 1
    assert trie.count_words_with_suffix("a") == 1
    assert trie.count_words_with_suffix("at") == 1

    assert trie.has_prefix("app") == True
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True
    assert trie.has_prefix("ca") == True

    print("All assertions passed!")
