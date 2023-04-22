class YALLexer:
    def __init__(self, filename):
        self.variables = {}
        self.individuals = {}
        self.operator = set()
        self.filename = filename
        self.convertToSomething()
        with open(filename, 'r') as f:
            self.file_contents = f.read()
        
    def extractVariables(self):
        # Extracts variables from the line
        # and stores them in the dictionary
        # self.variables
        lines = self.file_contents.readlines()
        for line in lines:
            if line.startswith('let'):
                varName, varValue = self.getVar(line)
                VarRe = self.ConvertToRegex(varValue)
                self.variables[varName] = VarRe
                
        
