class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.variables = []
        
    def parse(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.tokens.append(line)
                
        ws = ' \t\n'
        id = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        plus = '+'
        times = '*'
        lparen = '('
        rparen = ')'
        
