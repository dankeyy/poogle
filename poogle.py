import ast

def main():
    test = "(x: int, y: str) -> str"
    query = "def f" + test + ":..."
    parsed = ast.parse(query)
    # print(ast.dump(parsed, indent=4))
    func = parsed.body[0]

    arg_types = tuple(x.annotation.id for x in func.args.args)
    return_type = func.returns.id

    print(arg_types, return_type)

if __name__ == '__main__':
    main()
