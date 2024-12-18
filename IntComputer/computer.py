class IntComputer:
    def __init__(self, program, input_piped_mode=False, output_piped_mode=False):
        self.program = program
        self.instr = 0
        self.piped_input = []
        self.input_piped_mode = input_piped_mode
        self.piped_output = []
        self.output_piped_mode = output_piped_mode

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
            99: 0
        }
        return codes[code]

    def parse_op_code(self, op):
        code = op%100
        op //= 100
        modes = []
        amount = self.code_to_param_count(code)
        while len(modes) < amount:
            modes.append(op%10)
            op //= 10
        return code, modes

    def run_program(self):
        code = 0
        while code != 99:
            op = self.program[self.instr]
            code, modes = self.parse_op_code(op)
            values = []
            for i, m in enumerate(modes):
                values.append((self.program[self.instr+i+1], m))
            if code == 1:
                self.addition(values)
                self.instr += 4
            elif code == 2:
                self.multiplication(values)
                self.instr += 4
            elif code == 3:
                if self.input_piped_mode and self.piped_input == []:
                    break
                self.input(values)
                self.instr += 2
            elif code == 4:
                self.output(values)
                self.instr += 2
            elif code == 5:
                jumped = self.jump_if_true(values)
                self.instr += 3 if not jumped else 0
            elif code == 6:
                jumped = self.jump_if_false(values)
                self.instr += 3 if not jumped else 0
            elif code == 7:
                self.less_than(values)
                self.instr += 4
            elif code == 8:
                self.equals(values)
                self.instr += 4
        return code == 99

    def result(self):
        return self.program[0]

    def addition(self, values):
        left = self.get_value(values[0])
        right = self.get_value(values[1])
        result = left + right
        position = values[2][0]
        self.program[position] = result

    def multiplication(self, values):
        left = self.get_value(values[0])
        right = self.get_value(values[1])
        result = left * right
        position = values[2][0]
        self.program[position] = result

    def input(self, values):
        self.program[values[0][0]] = self.get_input()

    def output(self, values):
        out = self.get_value(values[0])
        if self.piped_output is not None:
            self.piped_output.append(out)
        else:
            print(out)

    def jump_if_true(self, values):
        val = self.get_value(values[0])
        jump_point = self.get_value(values[1])
        if val != 0:
            self.instr = jump_point
            return True
        return False

    def jump_if_false(self, values):
        val = self.get_value(values[0])
        jump_point = self.get_value(values[1])
        if val == 0:
            self.instr = jump_point
            return True
        return False

    def less_than(self, values):
        left = self.get_value(values[0])
        right = self.get_value(values[1])
        position = values[2][0]
        self.program[position] = 1 if left < right else 0

    def equals(self, values):
        left = self.get_value(values[0])
        right = self.get_value(values[1])
        position = values[2][0]
        self.program[position] = 1 if left == right else 0

    def get_value(self, v):
        if v[1] == 0:
            return self.program[v[0]]
        else:
            return v[0]

    def get_input(self):
        if self.piped_input:
            return self.piped_input.pop(0)
        else:
            return int(input())

    def get_output(self):
        return self.piped_output