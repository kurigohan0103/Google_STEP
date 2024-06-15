from load_dictionary import DictionaryLoader

class AnagramSolver:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def sort_word(self, word):
        return sorted(word)

    def sort_dictionary(self):
        new_dictionary = []
        for word in self.dictionary:
            sorted_word = ''.join(self.sort_word(word))
            new_dictionary.append((sorted_word, word))
        new_dictionary.sort()
        return new_dictionary

    def binary_search(self, data, target):
        left, right = 0, len(data) - 1
        while left <= right:
            middle = (left + right) // 2
            if data[middle][0] == target:
                # 一致するすべてのアナグラムを収集
                results = []
                # 左側を探索
                idx = middle
                while idx >= left and data[idx][0] == target:
                    results.append(data[idx][1])
                    idx -= 1
                # 右側を探索
                idx = middle + 1
                while idx <= right and data[idx][0] == target:
                    results.append(data[idx][1])
                    idx += 1
                return results
            elif data[middle][0] < target:
                left = middle + 1
            else:
                right = middle - 1
        return []

    def find_anagrams(self, random_word):
        sorted_word = ''.join(self.sort_word(random_word))
        new_dictionary = self.prepare_dictionary()
        return self.binary_search(new_dictionary, sorted_word)

# 使用例
file_path = 'G:\\マイドライブ\\趣味\\GoogleSTEP\\week1\\words.txt'
loader = DictionaryLoader(file_path)
dictionary = loader.load_words()

solver = AnagramSolver(dictionary)
print(solver.find_anagrams('solve'))


# # ファイルから単語を読み込み、改行で分割してリストにする
# with open('G:\マイドライブ\趣味\GoogleSTEP\week1\words.txt', 'r') as file:
#     dictionary1 = file.read().strip().split()
# print(dictionary1)
#
# def better_solution(random_word, dictionary):
#
#     # 単語をアルファベット順にソート
#     sorted_word = sorted(random_word)
#
#     new_dictionary = []
#     for word in dictionary:
#         new_dictionary.append(sorted(word), word)
#
#     # 辞書をアルファベット順にソート
#     new_dictionary.sort()
#
#     # 二分探索して元の単語を返す
#     anagram = binary_search(new_dictionary, sorted_word)
#
#
#     return anagram
#
# def binary_search(data, target):
#     left = 0
#     right = len(data)-1
#
#     while left < right:
#         midle = (left + right) / 2
#         if data[midle] == target:
#             return
#         elif data[midle] < target:
#             left = midle + 1
#         else:
#             right = midle - 1
#     return None



