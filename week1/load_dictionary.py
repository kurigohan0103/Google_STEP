class DictionaryLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_words(self):
        with open(self.file_path, 'r') as file:
            dictionary = file.read().strip().split()
        return dictionary
