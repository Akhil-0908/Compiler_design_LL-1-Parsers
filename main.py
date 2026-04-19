from input.grammar_input import get_grammar
from input.string_input import get_input_string

from grammar.grammar import Grammar
from grammar.first_follow import FirstFollow
from grammar.preprocess import Preprocess

from lexer.lexer import Lexer

from parsers.recursive_decent import RecursiveDescentParser
from parsers.ll1_parser import LL1Parser
from parsers.operator_precedance import OperatorPrecedenceParser
from parsers.slr_parser import SLRParser
from parsers.clr_parser import CLRParser
from parsers.lalr_parser import LALRParser


def main():
    # ---------------- LOAD GRAMMAR ---------------- #
    productions = get_grammar()
    grammar = Grammar(productions)

    # ---------------- INPUT STRING ---------------- #
    input_string = get_input_string()

    lexer = Lexer()
    tokens = lexer.tokenize(input_string)
    print("\nTokens:", tokens)

    # ---------------- MENU ---------------- #
    print("\nChoose Parser:")
    print("1. Recursive Descent")
    print("2. LL(1)")
    print("3. Operator Precedence")
    print("4. SLR")
    print("5. CLR")
    print("6. LALR")

    choice = int(input("Enter choice: "))

    # ---------------- PARSERS ---------------- #

    # 1. Recursive Descent
    if choice == 1:
        RecursiveDescentParser(tokens).parse()

    # 2. LL(1)
    elif choice == 2:
        grammar.print_grammar("Original Grammar")

        preprocess = Preprocess()

        # Remove Left Recursion
        grammar = preprocess.remove_left_recursion(grammar)
        grammar.print_grammar("After Removing Left Recursion")

        # Left Factoring
        grammar = preprocess.left_factoring(grammar)
        grammar.print_grammar("After Left Factoring")

        # FIRST & FOLLOW
        ff = FirstFollow(grammar)

        LL1Parser(grammar, ff, tokens).parse()

    # 3. Operator Precedence
    elif choice == 3:
        print("\nPreparing Operator Precedence Parser...\n")

        opg_grammar = {}

        # ✅ No split here (productions already list)
        for head in grammar.productions:
            opg_grammar[head] = []
            for prod in grammar.productions[head]:
                opg_grammar[head].append(prod)

        # Start symbol
        start_symbol = list(opg_grammar.keys())[0]

        parser = OperatorPrecedenceParser(opg_grammar, start_symbol, tokens)

        # Validate grammar
        if not parser.is_operator_grammar():
            print("❌ Given grammar is NOT suitable for Operator Precedence Parsing")
        else:
            parser.parse()

    # 4. SLR
    elif choice == 4:
        SLRParser(grammar, tokens).parse()

    # 5. CLR
    elif choice == 5:
        CLRParser(grammar, tokens).parse()

    # 6. LALR
    elif choice == 6:
        LALRParser(grammar, tokens).parse()

    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()