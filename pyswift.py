from compiletools import tokenize, parse, generate_code
import sys
def compile(src_path, output_name):
    input = None
    with open(src_path, "r", encoding = 'utf-8') as f:
        input = f.read()
    assert type(input) is not None
    tokens = tokenize(input)
    tokens_ids = [token.id for token in tokens]
    parsing = parse(tokens_ids)
    if parsing is not None:
        generate_code(output_name, tokens)

if __name__ == '__main__':
    args = sys.argv[1:]
    assert len(args) == 2
    compile(args[0], args[1])
