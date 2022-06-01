import ast

def main():
    test = "(x: int, y: str) -> str"
    query = "def f" + test + ":..."
    print(ast.dump(ast.parse(query), indent=4))


if __name__ == '__main__':
    main()
