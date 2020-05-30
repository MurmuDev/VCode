import re

RegDict =  {r'(\S+)+\s*=\s*(\S+)+(?!\(\))':0,                   #x = y
            r'from?\s+(S+)+\s+import\s+(\S*)':1,       #import
            r'^(def)\s*(\S+)\((.*?)\)':2,                     #function/method
            r'\s*class\s+(\S+):':3,                           #class
            r'(\S+)+\.(\w+)+\((\S+)*\)$':4,               #calling.called()
            r'import\s+(\S*)':5  ,
            r'Return\s+(.+)+':6,
            r'(\S+)+\s*=\s*(\S+)+\((.*?)\)$':7  ,          #callling = called()
            r'(?!=)(\w+)+\((\S+)*\)':8 ,                          #caller()
            }

def compareReg(reg,line):
    x = re.compile(reg)
    regobj = x.search(line)
    if regobj is None:
        return None
    else:
        return regobj.groups()



def regexCheck(line):
    global RegDict
    for x,y in RegDict.items():
        groups = compareReg(x,line)
        if groups is not None:
            return groups + (y,)
    return ''
