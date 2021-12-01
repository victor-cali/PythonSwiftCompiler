from dataclasses import dataclass
from typing import Union, Tuple, List
import re


@dataclass(frozen=True)
class Token:
    id: str
    val: Union[Tuple[str],str]


def tokenize(input: str) -> list:

    loopstruct_values = []
    printstruct_values = []
    
    vocabulary = {
        'if', 'for', 'in', 'range(', 'string',
        'print(', ')', ':', ','
    } # value and identifier are omitted as it is easier to find them separately

    strings_list = re.findall('".*"'+'|'+"'.*'", input)
    input = re.sub('".*"'+'|'+"'.*'", "string", input)
    input = re.sub("\(", "( ", input)
    input = re.sub("\)", " ) ", input)
    input = re.sub(":", " : ", input)
    input = re.sub(",", " , ", input)

    input = input.split()

    tokens = []
    for lexemme in input:
        if lexemme in vocabulary:
            if lexemme == 'string':
                string = strings_list.pop()
                printstruct_values.append(string)
            tokens.append(lexemme)
        elif lexemme.isidentifier():
            if tokens[-1] == 'for':
                loopstruct_values.append(lexemme)
            elif tokens[-1] == 'print(':
                printstruct_values.append(lexemme)
            tokens.append("identifier")
        elif lexemme.isnumeric():
            if lexemme != '0' and lexemme[0] == '0':
                raise SyntaxError(f'Invalid token at first position of {lexemme}')
            else:
                if tokens[-1] in {'range(',','}:
                    loopstruct_values.append(lexemme)
                elif tokens[-1] == 'print(':
                    printstruct_values.append(lexemme)
                tokens.append("value")  
        else:
            raise SyntaxError(f'Invalid token: {lexemme}')

    tokens = ''.join(tokens)
    tokens = re.sub('foridentifierinrange\(value,value\):', " c ", tokens)
    tokens = re.sub('print\(identifier\)|print\(string\)', " p ", tokens)
    tokens = tokens.split()
    token_list = []
    for token in tokens:
        if token == 'c':
            vals = [loopstruct_values.pop(0) for i in range(3)]
            vals = tuple(vals)
        if token == 'p':
            vals = printstruct_values.pop(0)
        token_list.append(Token(token,vals))

    for token in token_list:
        print(token.id, token.val)
    print()
    
    return token_list


def parse(tokens: list) -> bool:

    errors = (
        'Unknown error while parsing', 
        'Invalid syntax, cannot start with print statement', 
        'Unexpected EOF while parsing',
        'Invalid syntax, cannot end with for statement'
    )
    rules = ('L', 'E', 'E', 'E')
    tokens.append('$')
    symbols = []
    states = [0]

    def shift(state: int) -> None:
        print(f'shift {state}')
        states.append(state)
        symbol = tokens.pop(0)
        symbols.append(symbol)
    def reduce(rule: int) -> None:
        print(f'reduce {rule}')
        states.pop()
        symbols.pop()
        symbol = rules[rule]
        symbols.append(symbol)
        state = states[-1]
        arg = arg_table[symbol][state]
        func = func_table[symbol][state]
        func(arg)
    def goto(state: int) -> None:
        print(f'goto {state}')
        states.append(state)
    def error(err: int) -> None:
        error = errors[err]
        raise SyntaxError(error)
    def accept(*args) -> None:
        return('Accepted')

    func_table = {
        'c': (shift, reduce, shift, reduce, reduce, reduce),
        'p': (error, reduce, shift, reduce, reduce, reduce),
        '$': (error, accept, error, reduce, reduce, reduce),
        'L': (goto, error, goto, error, error, error),
        'E': (goto, error, goto, error, error, error)
    }
    arg_table = {
        'c': (3, 2, 5, 3, 0, 1),
        'p': (1, 2, 4, 3, 0, 1),
        '$': (2, 0, 3, 3, 0, 1),
        'L': (1, -1, 1, -1, -1, -1),
        'E': (2, -1, 2, -1, -1, -1)
    }

    finished = False
    while not finished:
        print('pointer:    ', tokens[0])
        print('Symbol stack:    ', symbols)
        print('State stack: ', states)
        symbol = tokens[0]
        state = states[-1]
        arg = arg_table[symbol][state]
        func = func_table[symbol][state]
        parsing_state = func(arg)
        if parsing_state is not None:
            print(parsing_state)
            finished = True
    return parsing_state


def generate_code(output_name: str, tokens: List[Token]):
    code = []
    tabs = ''
    for token in tokens:
        if token.id == 'c':
            start = f'{tabs}for {token.val[0]} in {token.val[1]}..<{token.val[2]} ' + '{\n'
            end = f'{tabs}' + '}\n'
            if len(code) == 0:
                code.append(start)
                code.append(end)
            else:
                pos = None
                for i in range(len(code)):
                    if code[i][-2] == '}':
                        pos = i
                        break
                assert pos is not None
                code.insert(pos,end)
                code.insert(pos,start)
            tabs += '\t'
        if token.id == 'p':
            pos = None
            line = f'{tabs}print({token.val})\n'
            for i in range(len(code)):
                if code[i][-2] == '}':
                    pos = i
                    break
            assert pos is not None
            code.insert(pos,line)             
    code = ''.join(code)

    with open(output_name, "w", encoding = 'utf-8') as f:
        f.write(code)