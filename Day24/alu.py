from typing import Sequence


class Alu:
    def __init__(self, memory: Sequence):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.memory = memory
        self.index = 0

    def __getitem__(self, item: str) -> int:
        match item:
            case 'w':
                return self.w
            case 'x':
                return self.x
            case 'y':
                return self.y
            case 'z':
                return self.z
            case _:
                raise KeyError

    def __setitem__(self, item: str, value: int | str):
        match item:
            case 'w':
                self.w = int(value)
            case 'x':
                self.x = int(value)
            case 'y':
                self.y = int(value)
            case 'z':
                self.z = int(value)
            case _:
                raise KeyError

    def __str__(self) -> str:
        return f"w = {self.w}\nx = {self.x}\ny = {self.y}\nz = {self.z}"

    def inp(self, r: str):
        self[r] = self.memory[self.index]
        self.index += 1

    def add(self, r: str, v: str):
        try:
            v_int = int(v)
        except ValueError:
            v_int = self[v]
        self[r] += v_int

    def mul(self, r: str, v: str):
        try:
            v_int = int(v)
        except ValueError:
            v_int = self[v]
        self[r] *= v_int

    def div(self, r: str, v: str):
        try:
            v_int = int(v)
        except ValueError:
            v_int = self[v]
        self[r] //= v_int

    def mod(self, r: str, v: str):
        try:
            v_int = int(v)
        except ValueError:
            v_int = self[v]
        self[r] %= v_int

    def eql(self, r: str, v: str):
        try:
            v_int = int(v)
        except ValueError:
            v_int = self[v]
        self[r] = int(v_int == self[r])

    def parse(self, command: str):
        instruction = command.split(' ')
        match instruction:
            case ['inp', str(r)]:
                self.inp(r)
            case ['add', str(r), str(v)]:
                self.add(r, v)
            case ['mul', str(r), str(v)]:
                self.mul(r, v)
            case ['div', str(r), str(v)]:
                self.div(r, v)
            case ['mod', str(r), str(v)]:
                self.mod(r, v)
            case ['eql', str(r), str(v)]:
                self.eql(r, v)
            case _:
                raise ValueError
