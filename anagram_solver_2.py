from collections import Counter
import os
from score_checker import calculate_score

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# fileを読み込む関数
def load_file(filename):
    with open(filename, 'r') as file:
        LoadedFile = file.read().strip().split()
    return LoadedFile


# アナグラムを見つける関数
def find_anagrams(word_list, dictionary):
    # 辞書単語のカウントを事前に計算
    dict_counts = {word: Counter(word) for word in dictionary}

    # アナグラムの結果
    anagrams = {word: [] for word in word_list}

    # 単語リストの各単語について
    for word in word_list:
        word_count = Counter(word)

        # 辞書の各単語と比較
        for dict_word, dict_count in dict_counts.items():
            if all(word_count[char] >= dict_count[char] for char in dict_count):
                anagrams[word].append(dict_word)

    return anagrams


# メイン処理
def main():
    word_dictionary = load_file('words.txt')
    word_list = load_file('large.txt')
    anagrams = find_anagrams(word_list, word_dictionary)


    output_filename = 'large_answer.txt'
    with open(output_filename, 'w', encoding='utf-8') as f:
        for word, anagram_list in anagrams.items():
            # 各アナグラムのスコアを計算し、最も高いスコアのものを選択
            if anagram_list:
                highest_score_anagram = max(anagram_list, key=calculate_score)
                f.write(f"{highest_score_anagram}\n")
            else:
                f.write("No anagrams found\n")


if __name__ == "__main__":
    main()
