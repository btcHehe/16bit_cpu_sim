from register import Register16, Register8


# class implementing processor operations on registers
class Processor:
    def __init__(self):
        self.AX = Register16('AX', 'AH', 'AL')
        self.BX = Register16('BX', 'BH', 'BL')
        self.CX = Register16('CX', 'CH', 'CL')
        self.DX = Register16('DX', 'DH', 'DL')
        self.C = 0
        self.Z = 0
        self.stack = []
        self.SP = 0
        self.IP = 0
        self.instructionList = ['MOV', 'ADD', 'SUB', 'JMP', 'JZ', 'JC', 'POP', 'PUSH', 'INC', 'DEC', 'OR', 'AND',
                                'XOR', 'CLR', 'ROR', 'ROL', 'SHR', 'SHL']
        self.registerList = [self.AX, self.BX, self.CX, self.DX]

    # method for finding register by its name
    def findReg(self, name):
        for reg in self.registerList:
            if reg.name.upper() == name.upper():
                return reg, None
            elif reg.H.name.upper() == name.upper():
                return reg, reg.H
            elif reg.L.name.upper() == name.upper():
                return reg, reg.L
        return None, None

    # addition operation
    def add(self, src, dest):
        if isinstance(src, int):
            dest.content += src
        else:
            dest.content += src.content
        if dest.content == 0:
            self.Z = 1
        else:
            self.Z = 0
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    c = r.update(False)
                    if c:
                        self.C = 1
                    else:
                        self.C = 0
                    break
        elif isinstance(dest, Register16):  # update NL and NH registers
            c = dest.update(True)
            if c:
                self.C = 1
            else:
                self.C = 0

    # subtraction operation
    def sub(self, src, dest):
        if isinstance(src, int):
            dest.content -= src
        else:
            dest.content -= src.content
        if dest.content == 0:
            self.Z = 1
        else:
            self.Z = 0
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    c = r.update(False)
                    if c:
                        self.C = 1
                    else:
                        self.C = 0
        elif isinstance(dest, Register16):  # update NL and NH registers
            c = dest.update(True)
            if c:
                self.C = 1
            else:
                self.C = 0

    # move operation
    def mov(self, src, dest):
        if isinstance(src, int):
            dest.content = src
        else:
            dest.content = src.content
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # push on stack operation
    def push(self, src):
        if isinstance(src, int):
            self.stack.append(src)
            self.SP += 1
        else:
            self.stack.append(src.content)
            self.SP += 1

    # pop from stack operation
    def pop(self, dest):
        if isinstance(dest, Register16):
            dest.content = self.stack.pop()
            self.SP -= 1
            dest.update(True)

    # unconditional jump operation
    def jmp(self, dest):
        if isinstance(dest, int):
            self.IP = dest

    # jump when zero flag is set operation
    def jz(self, dest):
        if isinstance(dest, int) and self.Z == 1:
            self.Z = 0
            self.IP = dest

    # jump when carry flag is set operation
    def jc(self, dest):
        if isinstance(dest, int) and self.C == 1:
            self.C = 0
            self.IP = dest

    # increment register opearation
    def inc(self, dest):
        if dest.content == 32766:
            self.C = 1
        else:
            self.C = 0
        dest.content += 1
        if dest.content == 0:
            self.Z = 1
        else:
            self.Z = 0
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # decrement register operation
    def dec(self, dest):
        if dest.content == 0:
            self.C = 1
        else:
            self.C = 0
        dest.content -= 1
        if dest.content == 0:
            self.Z = 1
        else:
            self.Z = 0
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # logical or opeartion
    def orl(self, src, dest):
        dest.content |= src.content
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # logical and operation
    def andl(self, src, dest):
        dest.content &= src.content
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # logical xor operation
    def xorl(self, src, dest):
        dest.content ^= src.content
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # clear register operation
    def clr(self, dest):
        dest.content = 0
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)
        elif isinstance(dest, int):
            dest = 0

    # rotate right operation
    def ror(self, dest):
        if isinstance(dest, Register8):
            dest.content = (2 ** 8 - 1) & (dest.content >> 1 | dest.content << (8 - 1))
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.content = (2 ** 16 - 1) & (dest.content >> 1 | dest.content << (16 - 1))
            dest.update(True)

    # rotate left operation
    def rol(self, dest):
        if isinstance(dest, Register8):
            dest.content = (2 ** 8 - 1) & (dest.content << 1 | dest.content >> (8 - 1))
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.content = (2 ** 16 - 1) & (dest.content << 1 | dest.content >> (16 - 1))
            dest.update(True)

    # shift right operation
    def shr(self, dest):
        dest.content >>= 1
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # shift left operation
    def shl(self, dest):
        dest.content <<= 1
        if isinstance(dest, Register8):
            dest.update()
            for r in self.registerList:
                if r.H.name == dest.name or r.L.name == dest.name:  # update 16 bit reg
                    r.update(False)
        elif isinstance(dest, Register16):  # update NL and NH registers
            dest.update(True)

    # debug method for printing actual values in registers
    def prt(self):
        print(f'AX: {self.AX.content}; AH: {self.AX.H.content}; AL: {self.AX.L.content}')
        print(f'BX: {self.BX.content}; BH: {self.BX.H.content}; BL: {self.BX.L.content}')
        print(f'CX: {self.CX.content}; CH: {self.CX.H.content}; CL: {self.CX.L.content}')
        print(f'DX: {self.DX.content}; DH: {self.DX.H.content}; DL: {self.DX.L.content}')
        print(f'C: {self.C}; Z: {self.Z}; IP: {self.IP}; SP: {self.SP}')
        print(f'Stack: {self.stack}')
        print('-'*40)
