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
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1

def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

def read_left_paren(line, index):
    token = {'type': 'LPAREN'}
    return token, index + 1

def read_right_paren(line, index):
    token = {'type': 'RPAREN'}
    return token, index + 1

def tokenize(line):
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
        elif line[index] == '(':
            (token, index) = read_left_paren(line, index)
        elif line[index] == ')':
            (token, index) = read_right_paren(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def change_rpn(tokens):
    # 最終的なRPN式を格納するキュー
    output_queue = []
    # 演算子と括弧を一時的に保持するスタック
    operator_stack = []
    # 各演算子の優先順位を定義する辞書
    precedence = {'PLUS': 1, 'MINUS': 1, 'MULTIPLICATION': 2, 'DIVISION': 2}
    for token in tokens:
        # 数字の場合、output_queue に追加
        if token['type'] == 'NUMBER':
            output_queue.append(token)
        # 演算子の場合
        elif token['type'] in ('PLUS', 'MINUS', 'MULTIPLICATION', 'DIVISION'):
            while (operator_stack and
                   operator_stack[-1]['type'] in precedence and
                   precedence[operator_stack[-1]['type']] >= precedence[token['type']]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        # 左括弧の場合、スタックに追加
        elif token['type'] == 'LPAREN':
            operator_stack.append(token)
        # 右括弧の場合、スタックに追加
        elif token['type'] == 'RPAREN':
            while operator_stack and operator_stack[-1]['type'] != 'LPAREN':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
    while operator_stack:
        output_queue.append(operator_stack.pop())
    return output_queue

def evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if token['type'] == 'NUMBER':
            stack.append(token['number'])
        elif token['type'] in ('PLUS', 'MINUS', 'MULTIPLICATION', 'DIVISION'):
            b = stack.pop()
            a = stack.pop()
            if token['type'] == 'PLUS':
                stack.append(a + b)
            elif token['type'] == 'MINUS':
                stack.append(a - b)
            elif token['type'] == 'MULTIPLICATION':
                stack.append(a * b)
            elif token['type'] == 'DIVISION':
                stack.append(a / b)
    return stack[0]

def evaluate(line):
    tokens = tokenize(line)
    rpn = change_rpn(tokens)
    return evaluate_rpn(rpn)

def test(line):
    actual_answer = evaluate(line)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

def run_test():
    print("==== Test started! ====")
    test("1")
    test("1+2")
    test("1.0+2")
    test("1.0+2.0")
    test("2*3+4")
    test("2+3*4")
    test("10/2+5")
    test("10+5/2")
    test("1-2")
    test("3*3")
    test("6/2")
    test("1+2*3-4/2")
    test("5-3+2*2")
    test("2.5*2")
    test("10/4+3*2-1")
    test("(1+2)*3")
    test("2*(3+4)")
    test("(2+3)*(4-2)/2")
    test("(3.0 + 4 * (2 - 1)) / 5")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    answer = evaluate(line)
    print("answer = %f\n" % answer)
