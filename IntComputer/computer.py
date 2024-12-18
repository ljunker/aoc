from collections import defaultdict


class IntComputer:
    def __init__(self, program, input_piped_mode=False, output_piped_mode=False):
        self.program = defaultdict(int)
        for i, v in enumerate(program):
            self.program[i] = v
        self.instr = 0
        self.piped_input = []
        self.input_piped_mode = input_piped_mode
        self.piped_output = []
        self.output_piped_mode = output_piped_mode
        self.relative_base = 0

    def code_to_param_count(self, code):
        codes = {
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 1,
            99: 0
        }
        return codes[code]

    def get_param(self, mode, reg):
        value = self.program[self.instr + reg]
        if mode == "0":
            return self.program[value]
        elif mode == "1":
            return value
        elif mode == "2":
            return self.program[self.relative_base + value]
        else:
            print("Error: Invalid Parameter Mode")

    def get_address(self, mode, reg):
        value = self.program[self.instr + reg]
        if mode == "0":
            return value
        elif mode == "2":
            return self.relative_base + value
        else:
            print("Error: Invalid Address Mode")

    def run_program(self):
        code = 0
        while code != 99:
            op = self.program[self.instr]
            code = op % 100
            m3, m2, m1 = f"{op // 100:03d}"
            if code == 1:
                self.program[self.get_address(m3, 3)] = self.get_param(m1, 1) + self.get_param(m2, 2)
                self.instr += 4
            elif code == 2:
                self.program[self.get_address(m3, 3)] = self.get_param(m1, 1) * self.get_param(m2, 2)
                self.instr += 4
            elif code == 3:
                if self.input_piped_mode and self.piped_input == []:
                    break
                self.input(self.get_address(m1, 1))
                self.instr += 2
            elif code == 4:
                self.output(self.get_param(m1, 1))
                self.instr += 2
            elif code == 5:
                if self.get_param(m1, 1) != 0:
                    self.instr = self.get_param(m2, 2)
                else:
                    self.instr += 3
            elif code == 6:
                if self.get_param(m1, 1) == 0:
                    self.instr = self.get_param(m2, 2)
                else:
                    self.instr += 3
            elif code == 7:
                self.program[self.get_address(m3, 3)] = int(
                    self.get_param(m1, 1) < self.get_param(m2, 2)
                )
                self.instr += 4
            elif code == 8:
                self.program[self.get_address(m3, 3)] = int(
                    self.get_param(m1, 1) == self.get_param(m2, 2)
                )
                self.instr += 4
            elif code == 9:
                self.relative_base += self.get_param(m1, 1)
                self.instr += 2
        return code == 99

    def result(self):
        return self.program[0]

    def input(self, address):
        self.program[address] = self.get_input()

    def output(self, out):
        if self.piped_output is not None and self.output_piped_mode:
            self.piped_output.append(out)
        else:
            print(out)

    def get_input(self):
        if self.piped_input and self.input_piped_mode:
            return self.piped_input.pop(0)
        else:
            return int(input())

    def get_output(self):
        return self.piped_output