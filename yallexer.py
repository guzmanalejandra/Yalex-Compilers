import re

class YalLexer:
    def __init__(self, filename):
        self.filename = filename
        self.regex = []
        self.comments = []
        self.rules = {}
        self.let = []
        self.rule_tokens = False

    def readfile(self):       
        with open(self.filename) as file:
            content = file.read().splitlines()

            for line in content:
                lineempty = line.strip()
                if lineempty == "":
                    continue
            
            for line in content:
                line = self.removecomments(line)
                lineempty = line.strip()

                comments = re.findall(r'\(\*(.*?)\*\)', line)
                if comments:
                    self.comments.extend(comments)
                    if not self.check_comments(comments):
                        print("Error: comentarios no cerrados correctamente" + line + "'")

                if line.startswith("let"):
                    key_value = line.split("=")
                    key = key_value[0].strip().split()[1]
                    value = key_value[1].strip()
                    
                    if YalLexer.checkBrackets(value):
                        print("Error"+ line)
                    
                  
                    self.let.append((key, value))
                    
                if line.startswith("rule tokens"):
                    self.rules = {}
                    self.rule_tokens = True
                    continue 
                
                if self.rule_tokens: 
                    tokens = re.findall(r'\|\s*([^\s\{\}]+)\s*\{[^\}]+\}', line)
                    for token in tokens:
                        self.rules[token] = token.lower()
                        if '{' in token and '}' not in token:
                            print("error" + line)
                        elif '}' in token and '{' not in token:
                            print("error" + line)

                    if line.endswith("};"):
                        self.rule_tokens = False
    
    def removecomments(self, line):
        if "(*" in line:
            line = line[:line.index("(*")] + line[line.index("*)") + 2:]
        return line
            
    def check_comments(self, comments):
        for comment in comments:
            if "(*" in comment and "*)" not in comment:
                return False
            if "*)" in comment and "(*" not in comment:
                return False
        return True
    
    @staticmethod
    def checkBrackets(string):
        stack = []
        opening = ["[", "("]
        closing = ["]", ")"]
        for char in string:
            if char in opening:
                stack.append(char)
            elif char in closing:
                if not stack:
                    return False
                elif opening.index(stack[-1]) != closing.index(char):
                    return False
                else:
                    stack.pop()
        if not stack:
            return True
        return False
    
    def build_regex(self):
        pass

                        



                    
