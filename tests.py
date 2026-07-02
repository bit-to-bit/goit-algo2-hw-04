from main1 import Homework
from main2 import LongestCommonWord

PASS = "PASS"
FAIL = "FAIL"


def run_test(name, actual, expected):
    status = PASS if actual == expected else FAIL
    print(f"  {status}  {name}")
    if actual != expected:
        print(f"         Expected: {expected!r}, Got: {actual!r}")


def run_exception_test(name, func, exception_type):
    try:
        func()
        print(
            f"  {FAIL}  {name} — expected {exception_type.__name__}, no exception raised"
        )
    except exception_type:
        print(f"  {PASS}  {name}")
    except Exception as e:
        print(f"  {FAIL}  {name} — unexpected exception: {type(e).__name__}: {e}")


def test_task1():
    print("\n" + "=" * 60)
    print("TASK 1 — Homework: count_words_with_suffix, has_prefix")
    print("=" * 60)

    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    print("\n[count_words_with_suffix]")
    run_test(
        'count_words_with_suffix("e") == 1  (apple)',
        trie.count_words_with_suffix("e"),
        1,
    )
    run_test(
        'count_words_with_suffix("ion") == 1  (application)',
        trie.count_words_with_suffix("ion"),
        1,
    )
    run_test(
        'count_words_with_suffix("a") == 1  (banana)',
        trie.count_words_with_suffix("a"),
        1,
    )
    run_test(
        'count_words_with_suffix("at") == 1  (cat)',
        trie.count_words_with_suffix("at"),
        1,
    )
    run_test(
        'count_words_with_suffix("le") == 1  (apple)',
        trie.count_words_with_suffix("le"),
        1,
    )
    run_test(
        'count_words_with_suffix("na") == 1  (banana)',
        trie.count_words_with_suffix("na"),
        1,
    )
    run_test(
        'count_words_with_suffix("xyz") == 0', trie.count_words_with_suffix("xyz"), 0
    )
    run_test(
        'count_words_with_suffix("apple") == 1  (full word)',
        trie.count_words_with_suffix("apple"),
        1,
    )

    print("\n[has_prefix]")
    run_test('has_prefix("app") == True', trie.has_prefix("app"), True)
    run_test('has_prefix("bat") == False', trie.has_prefix("bat"), False)
    run_test('has_prefix("ban") == True', trie.has_prefix("ban"), True)
    run_test('has_prefix("ca") == True', trie.has_prefix("ca"), True)
    run_test(
        'has_prefix("apple") == True  (full word as prefix)',
        trie.has_prefix("apple"),
        True,
    )
    run_test('has_prefix("xyz") == False', trie.has_prefix("xyz"), False)

    print("\n[Error handling]")
    run_exception_test(
        "count_words_with_suffix(123) raises TypeError",
        lambda: trie.count_words_with_suffix(123),
        TypeError,
    )
    run_exception_test(
        "count_words_with_suffix(None) raises TypeError",
        lambda: trie.count_words_with_suffix(None),
        TypeError,
    )
    run_exception_test(
        'count_words_with_suffix("") raises ValueError',
        lambda: trie.count_words_with_suffix(""),
        ValueError,
    )
    run_exception_test(
        "has_prefix(42) raises TypeError", lambda: trie.has_prefix(42), TypeError
    )
    run_exception_test(
        "has_prefix(None) raises TypeError", lambda: trie.has_prefix(None), TypeError
    )
    run_exception_test(
        'has_prefix("") raises ValueError', lambda: trie.has_prefix(""), ValueError
    )

    print("\n[Case sensitivity]")
    trie2 = Homework()
    trie2.put("Apple", 0)
    trie2.put("apple", 1)
    run_test(
        'count_words_with_suffix("Apple") == 1  (case sensitive)',
        trie2.count_words_with_suffix("Apple"),
        1,
    )
    run_test('has_prefix("App") == True', trie2.has_prefix("App"), True)
    run_test('has_prefix("app") == True', trie2.has_prefix("app"), True)
    run_test('has_prefix("APP") == False', trie2.has_prefix("APP"), False)


def test_task2():
    print("\n" + "=" * 60)
    print("TASK 2 — LongestCommonWord: find_longest_common_word")
    print("=" * 60)

    print("\n[Basic tests from assignment]")
    trie = LongestCommonWord()
    run_test(
        '["flower","flow","flight"] == "fl"',
        trie.find_longest_common_word(["flower", "flow", "flight"]),
        "fl",
    )

    trie = LongestCommonWord()
    run_test(
        '["interspecies","interstellar","interstate"] == "inters"',
        trie.find_longest_common_word(["interspecies", "interstellar", "interstate"]),
        "inters",
    )

    trie = LongestCommonWord()
    run_test(
        '["dog","racecar","car"] == ""',
        trie.find_longest_common_word(["dog", "racecar", "car"]),
        "",
    )

    print("\n[Edge cases]")
    trie = LongestCommonWord()
    run_test(
        '["hello"] == "hello"  (single word)',
        trie.find_longest_common_word(["hello"]),
        "hello",
    )

    trie = LongestCommonWord()
    run_test(
        '["abc","abc","abc"] == "abc"  (identical words)',
        trie.find_longest_common_word(["abc", "abc", "abc"]),
        "abc",
    )

    trie = LongestCommonWord()
    run_test(
        '["ab","abc"] == "ab"  (one is prefix of another)',
        trie.find_longest_common_word(["ab", "abc"]),
        "ab",
    )

    trie = LongestCommonWord()
    run_test(
        '["abc","ab"] == "ab"  (reverse order)',
        trie.find_longest_common_word(["abc", "ab"]),
        "ab",
    )

    print("\n[Invalid input handling]")
    trie = LongestCommonWord()
    run_test('[] == ""  (empty list)', trie.find_longest_common_word([]), "")

    trie = LongestCommonWord()
    run_test('None == ""', trie.find_longest_common_word(None), "")

    trie = LongestCommonWord()
    run_test(
        '"string" == ""  (not a list)', trie.find_longest_common_word("string"), ""
    )

    trie = LongestCommonWord()
    run_test(
        '["hello", 123] == ""  (non-string element)',
        trie.find_longest_common_word(["hello", 123]),
        "",
    )

    trie = LongestCommonWord()
    run_test(
        '[123, 456] == ""  (all non-strings)',
        trie.find_longest_common_word([123, 456]),
        "",
    )


if __name__ == "__main__":
    test_task1()
    test_task2()
    print("\n" + "=" * 60)
    print("All tests completed.")
    print("=" * 60)
