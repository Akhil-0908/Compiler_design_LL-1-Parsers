def get_grammar():
    print("Enter grammar (E -> E + T format). Type 'done' to finish:")
    productions = []
    while True:
        line = input().strip()
        if not line:
            continue
        if line.lower() == "done":
            break
        productions.append(line)
    return productions