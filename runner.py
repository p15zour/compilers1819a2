
import plex


class ParseError(Exception):
    pass


class RunError(Exception):
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

        self.st = {}

    def create_scanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.next_token()

    def next_token(self):
        return self.scanner.read()

    def match(self, token):
        if self.la == token:
            self.la, self.text = self.next_token()
        else:
            raise ParseError("self.la not similar with token!")

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
            raise ParseError("not 'identifier' or 'print' token!")

    def stmt(self):
        if self.la == "identifier":
            varname = self.text
            self.match("identifier")
            self.match("=")
            self.st[varname] = self.expr()
        elif self.la == "print":
            self.match("print")
            print('{:b}'.format(self.expr()))
        else:
            raise ParseError("wasn't the desirable!")

    def expr(self):
        if self.la in ("(", "identifier", "binary"):
            t = self.term()
            while self.la == "xor":
                self.match("xor")
                t2 = self.term()
                t ^= t2
            if self.la in ("identifier", "print", ")", None):
                return t
            raise ParseError("wasn't the desirable!")
        else:
            raise ParseError("wasn't the desirable!")

    def term(self):
        if self.la in ("(", "identifier", "binary"):
            a = self.atom()
            while self.la == "or":
                self.match("or")
                a2 = self.atom()
                a |= a2
            if self.la in ("xor", "identifier", "print", ")", None):
                return a
            raise ParseError("wasn't the desirable!")
        else:
            raise ParseError("wasn't the desirable!")


    def factor(self):
        if self.la == "(":
            self.match("(")
            e = self.expr()
            self.match(")")
            return e
        elif self.la == "identifier":
            varname = self.text
            self.match("identifier")
            if varname in self.st:
                return self.st[varname]
            raise RunError("there is not the value in the Dictionary.")
        elif self.la == "binary":
            value = int(self.text, 2)
            self.match("binary")
            return value
        else:
            raise ParseError("wasn't the desirable!")

    def atom(self):
        if self.la in ("(", "identifier", "binary"):
            a = self.factor()
            while self.la == "and":
                self.match("and")
                a2 = self.factor()
                a += a2
            if self.la in ("xor", "or", "identifier", "print", ")", None):
                return a
            raise ParseError("wasn't the desirable!")
        else:
            raise ParseError("wasn't the desirable!")

   

parser = myParser()
with open("testParser.txt") as fp:
    parser.parse(fp)

