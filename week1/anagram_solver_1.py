with open('words.txt', 'r') as file:
    word_dictionary = file.read().strip().split()


def AnagramSolver(random_word, dictionary):

    # 単語をアルファベット順にソート
    sorted_word = ''.join(sorted(random_word))

    # 辞書をアルファベット順にソートする
    sorted_dictionary = []
    for word in word_dictionary:
        sorted_dictionary_word = ''.join(sorted(word))
        sorted_dictionary.append((sorted_dictionary_word, word))
    sorted_dictionary.sort()

    # 二分探索
    left = 0
    right = len(sorted_dictionary)-1
    anagram = []

    while left <= right:
        middle = (left + right) // 2
        if sorted_word == sorted_dictionary[middle][0]:
            index = middle
            # 左側
            while index >= 0 and sorted_word == sorted_dictionary[index][0]:
                if sorted_dictionary[index][1] != random_word:
                    anagram.append(sorted_dictionary[index][1])
                index -= 1
            # 右側
            index = middle + 1
            while index < len(sorted_dictionary) and sorted_word == sorted_dictionary[index][0]:
                if sorted_dictionary[index][1] != random_word:
                   anagram.append(sorted_dictionary[index][1])
                index += 1
            break

        elif sorted_word > sorted_dictionary[middle][0]:
            left = middle + 1
        else:
            right = middle - 1

    if not anagram:
        return "No anagrams found."

    return anagram


if __name__ == "__main__":
    print(AnagramSolver('abel', word_dictionary))
    print(AnagramSolver('stop', word_dictionary))
    print(AnagramSolver('aaaa', word_dictionary))
    print(AnagramSolver('', word_dictionary))
    print(AnagramSolver('a', word_dictionary))
    print(AnagramSolver('zymurgy', word_dictionary))
    print(AnagramSolver('abcderghjiihhhhukpkjhhvfrrfcdghnjkjhgtgbnmkkjnbgyjmmnb', word_dictionary))
