from processor import Processor
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from cpu_parser import Parser
from constants import *
import re


# GUI of the simulator
class App(tk.Tk):
    def __init__(self, w, h):
        super().__init__()
        self.geometry(str(w) + 'x' + str(h))
        # self.attributes('-type', 'dialog')        # works on Linux but not on Windows
        self.title('16-bit processor simulator')
        self.editor = None
        self.lineNum = 0
        self.LineAmount = 0
        self.processor = Processor()
        self.parser = Parser()
        self.AXval = tk.StringVar()
        self.AXval.set(self.processor.AX.contentStr)
        self.BXval = tk.StringVar()
        self.BXval.set(self.processor.BX.contentStr)
        self.CXval = tk.StringVar()
        self.CXval.set(self.processor.CX.contentStr)
        self.DXval = tk.StringVar()
        self.DXval.set(self.processor.DX.contentStr)
        self.Cval = tk.StringVar()
        self.Cval.set(str(self.processor.C))
        self.Zval = tk.StringVar()
        self.Zval.set(str(self.processor.Z))
        self.IPval = tk.StringVar()
        self.StackGui = None
        self.IPval.set(str(self.processor.IP))
        self.SPval = tk.StringVar()
        self.SPval.set(str(self.processor.SP))
        self.lineNumVal = tk.StringVar()
        self.lineNumVal.set(str(self.lineNum))
        self.LabelDict = {}

    def updateStackGUI(self):
        self.StackGui.delete('1.0', 'end')
        for elem in list(reversed(self.processor.stack)):
            self.StackGui.insert(tk.INSERT, str(elem)+'\n')

    def spawnWidgets(self):
        self.editor = tk.Text(self, font=('Arial', 12, 'bold'), height=34, width=50)
        self.StackGui = tk.Text(self, font=('Arial', 14, 'bold'), height=8, width=15)
        self.updateStackGUI()

        loadButton = tk.Button(self, font=buttFont, text='Load code', height=BUTTON_H, width=BUTTON_W,
                               command=self.openFile)
        saveButton = tk.Button(self, font=buttFont, text='Save to file', height=BUTTON_H, width=BUTTON_W, command=self.saveFile)
        runButton = tk.Button(self, font=buttFont, text='Start', height=BUTTON_H, width=BUTTON_W, command=self.startProgram)
        stepButton = tk.Button(self, font=buttFont, text='Step', height=BUTTON_H, width=BUTTON_W, command=self.step)
        resetButton = tk.Button(self, font=buttFont, text='RESET', height=BUTTON_H, width=BUTTON_W, command=self.resetProgram)
        findButton = tk.Button(self, font=buttFont, text='Find labels', height=BUTTON_H, width=BUTTON_W,
                               command=lambda: self.parser.findLabels(self.editor.get(1.0, 'end-1c'), self.LabelDict))

        regLabel = tk.Label(self, font=('Arial', 18, 'bold'), text='Registers')
        AXlabel = tk.Label(self, font=labFont, text='AX: ')
        AXlabelValue = tk.Label(self, font=labValFont, textvariable=self.AXval)
        BXlabel = tk.Label(self, font=labFont, text='BX: ')
        BXlabelValue = tk.Label(self, font=labValFont, textvariable=self.BXval)
        CXlabel = tk.Label(self, font=labFont, text='CX: ')
        CXlabelValue = tk.Label(self, font=labValFont, textvariable=self.CXval)
        DXlabel = tk.Label(self, font=labFont, text='DX: ')
        DXlabelValue = tk.Label(self, font=labValFont, textvariable=self.DXval)

        stackLabel = tk.Label(self, font=('Arial', 18, 'bold'), text='Stack')

        flagsLabel = tk.Label(self, font=('Arial', 18, 'bold'), text='Flags & pointers')
        Clabel = tk.Label(self, font=labFont, text='C: ')
        ClabelVal = tk.Label(self, font=labValFont, textvariable=self.Cval)
        Zlabel = tk.Label(self, font=labFont, text='Z: ')
        ZlabelVal = tk.Label(self, font=labValFont, textvariable=self.Zval)
        IPlabel = tk.Label(self, font=labFont, text='IP: ')
        IPlabelVal = tk.Label(self, font=labValFont, textvariable=self.IPval)
        SPlabel = tk.Label(self, font=labFont, text='SP: ')
        SPlabelVal = tk.Label(self, font=labValFont, textvariable=self.SPval)

        lineNumLabel = tk.Label(self, font=labFont, text='Line number: ')
        lineNumVal = tk.Label(self, font=labValFont, textvariable=self.lineNumVal)

        self.editor.place(relx=0.03, rely=0.1)
        loadButton.place(relx=0.03, rely=0.02)
        saveButton.place(relx=0.11, rely=0.02)
        runButton.place(relx=0.19, rely=0.02)
        stepButton.place(relx=0.27, rely=0.02)
        resetButton.place(relx=0.35, rely=0.02)
        findButton.place(relx=0.43, rely=0.02)
        regLabel.place(relx=0.54, rely=0.02)
        AXlabel.place(relx=0.54, rely=0.1)
        BXlabel.place(relx=0.54, rely=0.15)
        CXlabel.place(relx=0.54, rely=0.2)
        DXlabel.place(relx=0.54, rely=0.25)
        AXlabelValue.place(relx=0.59, rely=0.1)
        BXlabelValue.place(relx=0.59, rely=0.15)
        CXlabelValue.place(relx=0.59, rely=0.2)
        DXlabelValue.place(relx=0.59, rely=0.25)

        stackLabel.place(relx=0.8, rely=0.02)
        self.StackGui.place(relx=0.75, rely=0.07)

        flagsLabel.place(relx=0.75, rely=0.312)
        Clabel.place(relx=0.75, rely=0.37)
        ClabelVal.place(relx=0.78, rely=0.37)
        Zlabel.place(relx=0.75, rely=0.41)
        ZlabelVal.place(relx=0.78, rely=0.41)
        IPlabel.place(relx=0.75, rely=0.45)
        IPlabelVal.place(relx=0.78, rely=0.45)
        SPlabel.place(relx=0.75, rely=0.49)
        SPlabelVal.place(relx=0.78, rely=0.49)

        lineNumLabel.place(relx=0.54, rely=0.32)
        lineNumVal.place(relx=0.68, rely=0.32)

    def openFile(self):
        fname = filedialog.askopenfilename(title='Open file with code', initialdir=os.getcwd(),
                                           filetypes=(("Assembly files", "*.asm"), ("all files", "*.*")))
        try:
            with open(fname) as file:
                self.editor.delete('1.0', 'end')      # clear editor
                for line in file:
                    self.editor.insert(tk.INSERT, line)

                self.LabelDict.clear()
                self.parser.findLabels(self.editor.get(1.0, 'end-1c'), self.LabelDict)      # reset label dictionary
                self.resetProgram()                                                         # reset cpu
        except:
            pass

    def saveFile(self):
        fname = filedialog.asksaveasfilename(initialfile='Untitled.asm', defaultextension='.asm',
                                             filetypes=(("Assembly files", "*.asm"), ("all files", "*.*")))
        try:
            file = open(fname, "w")
            text = self.editor.get(1.0, "end-1c")
            file.write(text)
            file.close()
        except:
            pass

    def update(self):
        self.AXval.set(self.processor.AX.content)
        self.BXval.set(self.processor.BX.content)
        self.CXval.set(self.processor.CX.content)
        self.DXval.set(self.processor.DX.content)
        self.Cval.set(str(self.processor.C))
        self.Zval.set(str(self.processor.Z))
        self.IPval.set(str(self.processor.IP))
        self.SPval.set(str(self.processor.SP))
        self.lineNumVal.set(str(self.lineNum))
        self.updateStackGUI()

    def readCode(self):
        lines = []
        txt = self.editor.get(1.0, "end-1c")
        txt = txt.split('\n')
        self.LineAmount = len(txt)
        for line in txt:
            lines.append(line)
        return lines

    def startProgram(self):
        self.parser.findLabels(self.editor.get(1.0, 'end-1c'), self.LabelDict)
        print(self.LabelDict)
        txt = self.readCode()
        notEnd = True
        while notEnd:
            self.highlightLine(self.lineNum)
            line = re.sub(r';.*', '', txt[self.lineNum])    # removing comments
            if not line:     # empty line
                self.processor.IP += 1
                self.lineNum += 1
                self.update()
                self.processor.prt()
                continue
            operands = self.parser.validate(line, self.LabelDict)
            if operands is None:
                return
            print(operands)
            if len(operands) == 1:
                if operands[0].upper() in self.LabelDict.keys():
                    self.processor.IP += 1
                    self.lineNum = self.processor.IP
                    return
            elif len(operands) == 2:
                if operands[0].upper() == 'JMP':
                    r, rPart = self.processor.findReg(operands[1])
                    if r is None and rPart is None:  # destination is label not register
                        self.processor.jmp(self.LabelDict[operands[1].upper()])
                        self.editor.tag_remove('highlight', float(self.lineNum + 1),
                                               str(float(self.lineNum + 1)) + ' lineend')
                        self.lineNum = self.processor.IP
                        self.editor.tag_add('highlight', float(self.lineNum + 1),
                                            str(float(self.lineNum + 1)) + ' lineend')
                        print('JUMPING')
                elif operands[0].upper() == 'JZ':
                    r, rPart = self.processor.findReg(operands[1])
                    if r is None and rPart is None:  # destination is label not register
                        self.processor.jz(self.LabelDict[operands[1].upper()])
                        self.editor.tag_remove('highlight', float(self.lineNum + 1),
                                               str(float(self.lineNum + 1)) + ' lineend')
                        self.lineNum = self.processor.IP
                        self.editor.tag_add('highlight', float(self.lineNum + 1),
                                            str(float(self.lineNum + 1)) + ' lineend')
                elif operands[0].upper() == 'JC':
                    r, rPart = self.processor.findReg(operands[1])
                    if r is None and rPart is None:  # destination is label not register
                        self.processor.jc(self.LabelDict[operands[1].upper()])
                        self.editor.tag_remove('highlight', float(self.lineNum + 1),
                                               str(float(self.lineNum + 1)) + ' lineend')
                        self.lineNum = self.processor.IP
                        self.editor.tag_add('highlight', float(self.lineNum + 1),
                                            str(float(self.lineNum + 1)) + ' lineend')
                elif operands[0].upper() == 'PUSH':
                    r, rPart = self.processor.findReg(operands[1])
                    if r is None:
                        self.processor.push(int(operands[1]))
                    else:
                        self.processor.push(r)
                elif operands[0].upper() == 'POP':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.pop(r)
                elif operands[0].upper() == 'INC':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.inc(r)
                elif operands[0].upper() == 'DEC':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.dec(r)
                elif operands[0].upper() == 'ROR':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.ror(r)
                elif operands[0].upper() == 'ROL':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.rol(r)
                elif operands[0].upper() == 'SHR':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.shr(r)
                elif operands[0].upper() == 'SHL':
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.shl(r)
                elif operands[0].upper() == 'CLR':
                    if operands[1].upper() == 'C':
                        self.processor.clr(self.processor.C)
                    elif operands[1].upper() == 'Z':
                        self.processor.clr(self.processor.Z)
                    else:
                        r, rPart = self.processor.findReg(operands[1])
                        self.processor.clr(r)
            elif len(operands) == 3:
                if isinstance(operands, list):
                    dst, dstPart = self.processor.findReg(operands[1])
                    if dstPart is not None:
                        destination = dstPart
                    else:
                        destination = dst
                    src, srcPart = self.processor.findReg(operands[2])
                    if src is None and srcPart is None:
                        source = int(operands[2])
                    else:
                        if srcPart is not None:
                            source = srcPart
                        else:
                            source = src
                    if operands[0].upper() == 'MOV':
                        self.processor.mov(source, destination)
                    elif operands[0].upper() == 'ADD':
                        self.processor.add(source, destination)
                    elif operands[0].upper() == 'SUB':
                        self.processor.sub(source, destination)
                    elif operands[0].upper() == 'OR':
                        self.processor.sub(source, destination)
                    elif operands[0].upper() == 'AND':
                        self.processor.sub(source, destination)
                    elif operands[0].upper() == 'XOR':
                        self.processor.sub(source, destination)
                else:
                    print(f'Error in line {self.lineNum}: {operands}')
            self.processor.IP += 1
            self.lineNum += 1
            self.processor.prt()
            self.update()

    def step(self):
        lines = self.readCode()
        if self.lineNum >= len(lines):
            return
        self.highlightLine(self.lineNum)
        line = re.sub(r';.*', '', lines[self.lineNum])  # removing comments
        if not line:        # empty line
            self.processor.IP += 1
            self.lineNum += 1
            self.update()
            self.processor.prt()
            return
        operands = self.parser.validate(line, self.LabelDict)
        if not isinstance(operands, list):
            messagebox.showerror(title='Error', message=operands)
            return
        if operands[0].upper() == 'END':
            return
        print(operands)
        if len(operands) == 1:
            if operands[0].upper() in self.LabelDict.keys():
                self.processor.IP += 1
                self.lineNum = self.processor.IP
                return
        elif len(operands) == 2:
            if operands[0].upper() == 'JMP':
                r, rPart = self.processor.findReg(operands[1])
                if r is None and rPart is None:     # destination is label not register
                    self.processor.jmp(self.LabelDict[operands[1].upper()])
                    self.editor.tag_remove('highlight', float(self.lineNum+1), str(float(self.lineNum+1)) + ' lineend')
                    self.lineNum = self.processor.IP
                    self.editor.tag_add('highlight', float(self.lineNum+1), str(float(self.lineNum+1)) + ' lineend')
                    print('JUMPING')
            elif operands[0].upper() == 'JZ':
                r, rPart = self.processor.findReg(operands[1])
                if r is None and rPart is None:     # destination is label not register
                    self.processor.jz(self.LabelDict[operands[1].upper()])
                    self.editor.tag_remove('highlight', float(self.lineNum+1), str(float(self.lineNum+1)) + ' lineend')
                    self.lineNum = self.processor.IP
                    self.editor.tag_add('highlight', float(self.lineNum+1), str(float(self.lineNum+1)) + ' lineend')
            elif operands[0].upper() == 'JC':
                r, rPart = self.processor.findReg(operands[1])
                if r is None and rPart is None:     # destination is label not register
                    self.processor.jc(self.LabelDict[operands[1].upper()])
                    self.editor.tag_remove('highlight', float(self.lineNum+1), str(float(self.lineNum+1)) + ' lineend')
                    self.lineNum = self.processor.IP
                    self.editor.tag_add('highlight', float(self.lineNum+1), str(float(self.lineNum+1)) + ' lineend')
            elif operands[0].upper() == 'PUSH':
                r, rPart = self.processor.findReg(operands[1])
                if r is None:
                    self.processor.push(int(operands[1]))
                else:
                    self.processor.push(r)
            elif operands[0].upper() == 'POP':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.pop(r)
            elif operands[0].upper() == 'INC':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.inc(r)
            elif operands[0].upper() == 'DEC':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.dec(r)
            elif operands[0].upper() == 'ROR':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.ror(r)
            elif operands[0].upper() == 'ROL':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.rol(r)
            elif operands[0].upper() == 'SHR':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.shr(r)
            elif operands[0].upper() == 'SHL':
                r, rPart = self.processor.findReg(operands[1])
                self.processor.shl(r)
            elif operands[0].upper() == 'CLR':
                if operands[1].upper() == 'C':
                    self.processor.clr(self.processor.C)
                elif operands[1].upper() == 'Z':
                    self.processor.clr(self.processor.Z)
                else:
                    r, rPart = self.processor.findReg(operands[1])
                    self.processor.clr(r)
        elif len(operands) == 3:
            if isinstance(operands, list):
                dst, dstPart = self.processor.findReg(operands[1])
                if dstPart is not None:
                    destination = dstPart
                else:
                    destination = dst
                src, srcPart = self.processor.findReg(operands[2])
                if src is None and srcPart is None:
                    source = int(operands[2])
                else:
                    if srcPart is not None:
                        source = srcPart
                    else:
                        source = src
                if operands[0].upper() == 'MOV':
                    self.processor.mov(source, destination)
                elif operands[0].upper() == 'ADD':
                    self.processor.add(source, destination)
                elif operands[0].upper() == 'SUB':
                    self.processor.sub(source, destination)
                elif operands[0].upper() == 'OR':
                    self.processor.sub(source, destination)
                elif operands[0].upper() == 'AND':
                    self.processor.sub(source, destination)
                elif operands[0].upper() == 'XOR':
                    self.processor.sub(source, destination)
            else:
                print(f'Error in line {self.lineNum}: {operands}')
        self.processor.IP += 1
        self.lineNum += 1
        self.update()
        self.processor.prt()

    def resetProgram(self):
        self.LabelDict.clear()
        self.parser.findLabels(self.editor.get(1.0, 'end-1c'), self.LabelDict)      # reset label dictionary
        self.editor.tag_remove('highlight', float(self.lineNum), str(float(self.lineNum))+' lineend')
        self.editor.tag_remove('highlight', float(self.LineAmount), str(float(self.LineAmount))+' lineend')
        self.lineNum = 0
        self.processor.IP = 0
        self.processor.Z = 0
        self.processor.C = 0
        self.highlightLine(self.lineNum)
        for r in self.processor.registerList:
            r.content = 0
            r.update(True)
        self.update()

    def highlightLine(self, lineNumber):
        prevTxt = self.editor.get(float(lineNumber), str(float(lineNumber))+' lineend')
        txt = self.editor.get(float(lineNumber+1), str(float(lineNumber+1))+' lineend')
        if prevTxt != txt:
            self.editor.tag_remove('highlight', float(lineNumber), str(float(lineNumber))+' lineend')
            self.editor.tag_add('highlight', float(lineNumber+1), str(float(lineNumber+1))+' lineend')
            self.editor.tag_config('highlight', background='green', foreground='red')
        else:
            self.editor.tag_add('highlight', float(lineNumber+1), str(float(lineNumber+1))+' lineend')
            self.editor.tag_config('highlight', background='green', foreground='red')
