def calculate_hash(key):
    assert type(key) == str
    hash = 0
    prime = 31  # プライム数を使用すると良い分散が得られることが多いです
    for char in key:
        hash = hash * prime + ord(char)
    return hash

# テスト
print(calculate_hash("alice"))
print(calculate_hash("elica"))