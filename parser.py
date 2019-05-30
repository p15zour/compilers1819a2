
import plex


class ParseError(Exception):
    pass


class myParser:
    def __init__(self):
        dig = plex.Range("09")
        dig1 = plex.Range("01")
        letter = plex.Range('azAZ')
        bit = plex.Rep1(dig1)
        name = letter + plex.Rep(letter | dig)
        and_tok = plex.Str("and")
        or_tok = plex.Str("or")
        xor_tok = plex.Str("xor")
        equal = plex.Str("=")
        open_par = plex.Str("(")
        close_par = plex.Str(")")
        print_tok = plex.Str("print")
        space = plex.Any(" \n\t")
        self.lexicon = plex.Lexicon([
            (space, plex.IGNORE),
            (bit, "binary"),
            (and_tok, "and"),
            (or_tok, "or"),
            (xor_tok, "xor"),
            (equal, "="),
            (print_tok, "print"),
            (open_par, "("),
            (close_par, ")"),
            (name, "identifier")])

    def create_scanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.next_token()

    def next_token(self):
        return self.scanner.read()

    def match(self, token):
        if self.la == token:
            self.la, self.text = self.next_token()
        else:
            raise ParseError("{} instead of {}!".format(self.la, token))

    def parse(self, fp):
        self.create_scanner(fp)
        self.stmt_list()

    def stmt_list(self):
        if self.la in ("identifier", "print"):
            self.stmt()
            self.stmt_list()
        elif self.la == None:
            return
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def stmt(self):
        if self.la == "identifier":
            self.match("identifier")
            self.match("=")
            self.expr()
        elif self.la == "print":
            self.match("print")
            self.expr()
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def expr(self):
        if self.la in ("(", "identifier", "binary"):
            self.term()
            self.term_tail()
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def term_tail(self):
        if self.la == "xor":
            self.match("xor")
            self.term()
            self.term_tail()
        elif self.la in ("identifier", "print", ")", None):
            return
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def term(self):
        if self.la in ("(", "identifier", "binary"):
            self.atom()
            self.atom_tail()
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def atom_tail(self):
        if self.la == "or":
            self.match("or")
            self.atom()
            self.atom_tail()
        elif self.la in ("xor", "identifier", "print", ")", None):
            return
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def atom(self):
        if self.la in ("(", "identifier", "binary"):
            self.factor()
            self.factor_tail()
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def factor_tail(self):
        if self.la == "and":
            self.match("and")
            self.factor()
            self.factor_tail()
        elif self.la in ("xor", "or", "identifier", "print", ")", None):
            return
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))

    def factor(self):
        if self.la == "(":
            self.match("(")
            self.expr()
            self.match(")")
        elif self.la == "identifier":
            self.match("identifier")
        elif self.la == "binary":
            self.match("binary")
        else:
            raise ParseError("{} wasn't the desirable!".format(self.la))


parser = myParser()
with open("testParser.txt") as fp:
    parser.parse(fp)


