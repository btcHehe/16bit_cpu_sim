class Register8:
    def __init__(self, name, content=0):
        self.MAX_VAL = 255
        self.content = content
        if content > self.MAX_VAL:
            self.content = 0
        elif content < 0:
            self.content = self.MAX_VAL
        self.name = name
        self.contentStr = str(content)

    def update(self, _f=True):
        ov = False
        if self.content > self.MAX_VAL:
            self.content = 0
            ov = True
        elif self.content < 0:
            self.content = self.MAX_VAL
            ov = True
        self.contentStr = str(self.content)
        return ov


class Register16:
    def __init__(self, name, hiName, lowName, content=0):
        self.MAX_VAL = 32766
        self.name = name
        self.H = Register8(hiName)
        self.L = Register8(lowName)
        tmp = (self.H.content << 8) + self.L.content
        if tmp > self.MAX_VAL:
            self.content = 0
        elif tmp < 0:
            self.content = self.MAX_VAL
        else:
            self.content = tmp
        self.contentStr = str(self.content)

    def update(self, split=False):
        if split:
            c = False
            if self.content > self.MAX_VAL:
                self.content = 0
                c = True
            elif self.content < 0:
                self.content = self.MAX_VAL
                c = True
            tmp = self.content >> 8
            self.H.content = tmp
            self.L.content = self.content & 0x00FF
            self.H.update()
            self.L.update()
            return c
        else:
            c = False
            self.content = (self.H.content << 8) + self.L.content
            if self.content > self.MAX_VAL:
                self.content = 0
                c = True
            elif self.content < 0:
                self.content = self.MAX_VAL
                c = True
            self.contentStr = str(self.content)
            return c
