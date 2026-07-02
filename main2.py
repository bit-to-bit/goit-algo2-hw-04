from trie import Trie


class LongestCommonWord(Trie):

    def find_longest_common_word(self, strings) -> str:
        if not isinstance(strings, list) or not strings:
            return ""
        if not all(isinstance(s, str) for s in strings):
            return ""
        for i, word in enumerate(strings):
            self.put(word, i)
        prefix = []
        node = self.root
        while len(node.children) == 1 and node.value is None:
            char = next(iter(node.children))
            prefix.append(char)
            node = node.children[char]
        return "".join(prefix)


if __name__ == "__main__":
    trie = LongestCommonWord()
    strings = ["flower", "flow", "flight"]
    assert trie.find_longest_common_word(strings) == "fl"

    trie = LongestCommonWord()
    strings = ["interspecies", "interstellar", "interstate"]
    assert trie.find_longest_common_word(strings) == "inters"

    trie = LongestCommonWord()
    strings = ["dog", "racecar", "car"]
    assert trie.find_longest_common_word(strings) == ""

    print("All assertions passed!")
