# This is a program that uses the ast module
# for parsing the program.
# The tree is then analysed for various tokens.


import ast
from pprint import pprint
import regex

# Analyzer class inherits the ast.NodeVisitor class
# check the python_grammar file to get the list of grammar
# the grammar can be used with the visit_x function
# x is to be found in the python_grammar file

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [],"call":[],"function":[],"class":[]}


    def visit_FunctionDef(self, node):
        name = node.name
        n = ''
        for x in node.body:
            n = 0
            x = str(x)
            t = regex.regexCheck(x)
            if t != '':
                l = len(t)
                y = t[l-1]
                if y == 6:
                    n = 1
        ftuple = (name,n,node.lineno)
        self.stats["function"].append(ftuple)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        x = node.name
        ftuple = (x,node.lineno)
        self.stats["class"].append(ftuple)
        self.generic_visit(node)

    def visit_Call(self, node):
        self.stats["call"].append(node.lineno)
        self.generic_visit(node)

    def visit_Import(self, node):
        for x in node.names:
            self.stats["import"].append(x.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for x in node.names:
            self.stats["import"].append(x.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


#prints the regex value of a line
def printRegexMatch(startline,endline):
    with open('./demo.py') as fp:
        line = fp.readline()
        while line and startline<=endline:
            s = line.strip()
            if len(s) != 0 and s[0] != '#':
                print(s+"-----"+str(regex.regexCheck(s)))
            line = fp.readline()
            startline = startline+1



#returns arguments/parameters of code
def returnArgs(lineno,address):
    with open(address) as fp:
        no = 1
        line = fp.readline()
        while int(no)<int(lineno) and line:
            line = fp.readline()
            no = no+1
        x = regex.regexCheck(line.strip())
        return x[2].split(',')



#returns a block of indented code starring for lineno
#address refers to file address
def returnBlock(lineno,address):
    block = []
    with open(address) as fp:
        no = 1
        line = fp.readline()
        while int(no)<int(lineno) and line:
            line = fp.readline()
            no = no+1
        block.append(line.strip())
        startIndent = (len(line.rstrip())-len(line.lstrip())+1)
        line = fp.readline()
        currentIndent = (len(line.rstrip())-len(line.lstrip())+1)
        while line and currentIndent>startIndent:
            s = line.strip()
            if len(s) != 0 and s[0] != '#':
                block.append(s)
            line = fp.readline()
            currentIndent = (len(line.rstrip())-len(line.lstrip())+1)
        return block

# print the block of code on given the block
def printBlock(block):
    for x in block:
        print(x)


#check the indentation level
#def checkIndent(lineno):

def main():
    #change file here
    file_address = 'demo.py'

    # The following code creates the parsing tree
    with open(file_address, "r") as source:
        tree = ast.parse(source.read())


    analyzer = Analyzer()  #created object for traversal
    analyzer.visit(tree)   #traveral
    analyzer.report()  #uncomment to get the list of found tokens
    classList = analyzer.stats["class"]
    funcList = analyzer.stats["function"]
    call_lines =  analyzer.stats["call"]

    callnameList = []   #store list of called
    for x in call_lines:
         b = returnBlock(x,file_address)
         for line in b:
             regx = regex.regexCheck(line)
             code = regx[len(regx)-1]
             if code == 4:
                 callnameList.append(regx[1])
             if code == 8:
                 callnameList.append(regx[0])
             if code == 7:
                 callnameList.append(regx[1])
    print(callnameList)
    for s in callnameList:  #search for callnames in funcList
        for x,y,z in funcList:
            if x==s:
                printBlock(returnBlock(z,file_address))

if __name__ == "__main__":
    main()
