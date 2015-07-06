import re
from string import hexdigits

__all__ = ['loads', 'load', 'parse']

class Parser(object):
    def __init__(self, text):
        self.stream = iter(text)
        self.ch = next(self.stream)
        self.EOS = False

    def accept(self, c):
        return self.ch == c

    def error(self):
        raise SyntaxError('Unexpected character:%s'% repr(self.ch))

    def expect(self, c):
        if not self.accept(c):
            self.error()
        self.advance()

    def advance(self):
        try:
            self.ch = self.stream.next()
        except StopIteration:
            self.EOS = True
            self.ch = ''

    def white(self):
        while re.match(r'\s|\n', self.ch):
            self.advance() 

    def parse_object(self):
        self.expect('{')
        self.white()
        obj = {}
        while not self.accept('}'):
            k, v = self.parse_pair()
            obj[k] = v
            self.white()
            if not self.accept('}'):
                self.expect(',')
                self.white()
        self.expect('}')
        return obj

    def parse_pair(self):
        k = self.parse_string()
        self.white()
        self.expect(':')
        self.white()
        v = self.parse_value()
        return k, v

    def parse_value(self):
        if self.accept('"'):
            return self.parse_string()
        elif re.match(r'-|\d', self.ch):
            return self.parse_number()
        elif self.accept('{'):
            return self.parse_object()
        elif self.accept('['):
            return self.parse_array()
        elif self.accept('t'):
            return self.parse_true()
        elif self.accept('f'):
            return self.parse_false()
        else:
            return self.parse_null()

    def parse_string(self):
        s = ''
        self.expect('"')
        while not self.accept('"'):
            if self.accept('\\'):
                self.advance()
                escaped = re.match(r'\"|\\|/|[bfnrt]', self.ch) 
                if escaped is not None:
                    char = self.ch
                elif self.accept('u'):
                    # parse something like \u1234
                    hex_digits = ''
                    for _ in xrange(4):
                        self.advance()
                        if self.ch not in hexdigits:
                            self.error() 
                        hex_digits += self.ch
                    self.advance()
                    char = unichr(int(hex_digits, 16))
                else:
                    self.error()
            else:
                char = self.ch
                self.advance()
            s += char
        self.expect('"')
        return s

    def parse_int(self):
        if self.accept('0'):
            # JSON doesn't accept numbers like this `0123`
            # so if we get a `0` in the beginning,
            # we assume the whole number is 0
            ret = self.ch
            self.advance()
            return ret
        else:
            return self.parse_digits()

    def parse_digits(self):
        s = ''
        while re.match(r'\d', self.ch):
            s += self.ch
            self.advance()
        return s

    def parse_frac(self):
        self.expect('.')
        return '.'+self.parse_digits()

    def parse_exp(self):
        s = 'e'
        self.advance()
        if self.accept('-') or self.accept('+'):
            s += self.ch
            self.advance()
        s += self.parse_digits()
        return s

    def parse_number(self):
        s = ''
        if self.accept('-'):
            s += '-'
            self.advance()
        s += self.parse_int()
        if self.accept('.'):
            s += self.parse_frac()
        if self.accept('e') or self.accept('E'):
            s += self.parse_exp()
        try:
            return int(s)
        except:
            return float(s)


    def parse_array(self):
        self.expect('[')
        self.white()
        arr = []
        while not self.accept(']'):
            arr.append(self.parse_value())
            self.white()
            if not self.accept(']'):
                self.expect(',')
                self.white()
        self.advance()
        return arr 

    def parse(self):
        ret = self.parse_value()
        self.white()
        if not self.EOS:
            self.error()
        return ret 

    def parse_null(self):
        self.expect('n')
        self.expect('u')
        self.expect('l')
        self.expect('l')
        return None

    def parse_false(self):
        self.expect('f')
        self.expect('a')
        self.expect('l')
        self.expect('s')
        self.expect('e')
        return False

    def parse_true(self):
        self.expect('t')
        self.expect('r')
        self.expect('u')
        self.expect('e')
        return True

def parse(text):
    return Parser(text).parse() 

loads = parse

def load(f):
    return loads(f.read())
