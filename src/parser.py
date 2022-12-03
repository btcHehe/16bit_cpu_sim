import re


class Parser:
    def __init__(self):
        self.registerList = ['AX', 'AH', 'AL', 'BX', 'BH', 'BL', 'CX', 'CH', 'CL', 'DX', 'DH', 'DL']
        self.instructionList2 = ['POP', 'PUSH', 'INC', 'DEC', 'ROR', 'ROL', 'SHR', 'SHL', 'CLR', 'JMP', 'JZ', 'JC']
        self.instructionList3 = ['MOV', 'ADD', 'SUB', 'AND', 'OR', 'XOR']

    def validate(self, line, labelsList):
        splitLine = line.split()
        if len(splitLine) == 3:
            if splitLine[0].upper() in self.instructionList3:
                if ',' in splitLine[1]:
                    splitLine[1] = splitLine[1].replace(',', '')
                    if splitLine[1].upper() in self.registerList:
                        return splitLine
                    else:
                        return f'Invalid argument: {splitLine[1]}'
                else:
                    return f'Comma between arguments missing'
            else:
                return f'Invalid instruction: {splitLine[0]}'
        elif len(splitLine) == 1:
            t = splitLine[0].replace(':', '')
            if t.upper() in labelsList.keys():
                return splitLine
        elif len(splitLine) == 2:
            if splitLine[0].upper() in self.instructionList2:
                return splitLine
            else:
                return f'Invalid instruction {splitLine[0]}'
        elif len(splitLine) < 1:
            return 'Too little operands'
        else:
            return 'Too many operands'

    def findLabels(self, code, labelsList):
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = re.sub(r';.*', '', line)  # removing comments
            splt = line.split()
            if len(splt) == 1:
                label = splt[0].replace(':', '')
                if label.upper() == 'END':
                    continue
                labelsList[label.upper()] = i
        print(labelsList)
