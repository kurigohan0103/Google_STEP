def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiplication(line, index):
    token = {'type': 'MULTIPLICATION'}  # タイポ修正
    return token, index + 1

def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

def tokenize(line):
    if not isinstance(line, str):
        raise TypeError("Expected a string, got a type of {}".format(type(line).__name__))
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def first_evaluate(tokens):
    result_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            result_tokens.append(tokens[index])
        elif tokens[index]['type'] == 'MULTIPLICATION':
            prev_number = result_tokens.pop()['number']
            next_number = tokens[index + 1]['number']
            result_tokens.append({'type': 'NUMBER', 'number': prev_number * next_number})
            index += 1  # スキップする
        elif tokens[index]['type'] == 'DIVISION':
            prev_number = result_tokens.pop()['number']
            next_number = tokens[index + 1]['number']
            result_tokens.append({'type': 'NUMBER', 'number': prev_number / next_number})
            index += 1  # スキップする
        else:
            result_tokens.append(tokens[index])
        index += 1
    return result_tokens

def second_evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # ダミーの '+' トークンを挿入
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate(line):
    tokens = tokenize(line)
    print("Tokens after tokenize:", tokens)  # トークンリストの内容を出力
    tokens = first_evaluate(tokens)
    print("Tokens after first_evaluate:", tokens)  # トークンリストの内容を出力
    return second_evaluate(tokens)

def test(line):
    actual_answer = evaluate(line)  # 文字列 `line` を直接 `evaluate` に渡す
    expected_answer = eval(line)  # eval 関数で期待される結果を計算
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("2*3+4")
    test("2+3*4")
    test("10/2+5")
    test("10+5/2")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    answer = evaluate(line)
    print("answer = %f\n" % answer)
