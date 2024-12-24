from itertools import permutations


class Wire:
    def __init__(self, name):
        self.name = name
        self.signal = None
        self.operation = None

    def get_value(self):
        if self.signal is None and self.operation:
            self.signal = self.operation.evaluate()
        return self.signal

    def set_signal(self, signal):
        self.signal = signal
        return self

class UnaryOperation:
    def __init__(self, operator, operand, output):
        self.operator = operator
        self.operand = operand
        self.output = output

    def evaluate(self):
        operand_value = self.operand.get_value()
        if self.operator == "NOT":
            return ~operand_value & 0xFFFF  # Mask for 16-bit result
        if self.operator == "ASSIGN":
            return operand_value
        raise ValueError(f"Unknown unary operator: {self.operator}")

class BinaryOperation:
    def __init__(self, operator, left, right, output):
        self.operator = operator
        self.left = left
        self.right = right
        self.output = output

    def evaluate(self):
        left_value = self.left.get_value()
        right_value = self.right.get_value()
        if self.operator == "AND":
            return left_value & right_value
        elif self.operator == "OR":
            return left_value | right_value
        elif self.operator == "XOR":
            return left_value ^ right_value
        raise ValueError(f"Unknown binary operator: {self.operator}")

class Circuit:
    def __init__(self):
        self.wires = {}

    def get_wire(self, name):
        if name not in self.wires:
            self.wires[name] = Wire(name)
        return self.wires[name]

    def add_instruction(self, instruction, pairs):
        parts = instruction.strip().split(" -> ")
        expression, target_name = parts[0], parts[1]
        if target_name in pairs:
            target_name = pairs[target_name]
        target_wire = self.get_wire(target_name)

        for operator in ["AND", "XOR", "OR"]:
            if operator in expression:
                left_name, right_name = expression.split(f" {operator} ")
                left_wire = self.get_wire(left_name) if not left_name.isdigit() else Wire(left_name)
                if left_wire.signal == None:
                    left_wire.signal = int(left_name) if left_name.isdigit() else None
                right_wire = self.get_wire(right_name) if not right_name.isdigit() else Wire(right_name)
                if right_wire.signal == None:
                    right_wire.signal = int(right_name) if right_name.isdigit() else None
                target_wire.operation = BinaryOperation(operator, left_wire, right_wire, target_wire)
                break

    def set_wire(self, target_name, target_wire):
        self.wires[target_name] = target_wire

    def evaluate(self, wire_name):
        wire = self.get_wire(wire_name)
        return wire.get_value()

    def evaluate_all(self):
        return {name: wire.get_value() for name, wire in self.wires.items()}


def parse_statements(statements):
    # Define the Graphviz input as a list of strings
    graphviz_lines = ["digraph LogicGraph {"]

    # Parse each statement and convert to Graphviz format
    for statement in statements.split("\n"):
        parts = statement.split("->")
        if len(parts) == 2:
            operation, output = parts[0].strip(), parts[1].strip()
            tokens = operation.split()
            if "AND" in tokens:
                inputs = operation.split("AND")
                node_label = "AND"
            elif "OR" in tokens:
                inputs = operation.split("OR")
                node_label = "OR"
            elif "XOR" in tokens:
                inputs = operation.split("XOR")
                node_label = "XOR"
            else:
                continue

            # Clean inputs and generate a gate node
            inputs = [inp.strip() for inp in inputs]
            gate_id = f"{inputs[0]}_{inputs[1]}_{node_label}"
            graphviz_lines.append(f'    {gate_id} [label="{node_label}", shape=box];')

            # Add edges from inputs to the gate
            for inp in inputs:
                graphviz_lines.append(f'    {inp} -> {gate_id};')

            # Add edge from gate to output
            graphviz_lines.append(f'    {gate_id} -> {output};')

    # Close the graph definition
    graphviz_lines.append("}")
    return "\n".join(graphviz_lines)


if __name__ == "__main__":
    starting, instructions = open("i.txt").read().strip().split("\n\n")
    circuit = Circuit()
    for i in instructions.split("\n"):
        circuit.add_instruction(i, {})
    for s in starting.split("\n"):
        name, value = s.split(": ")
        circuit.wires[name].set_signal(int(value))
    circuit.evaluate_all()
    pairs = {
        'z06': 'vwr',
        'vwr': 'z06',
        'z11': 'tqm',
        'tqm': 'z11',
        'z16': 'kfs',
        'kfs': 'z16'
    }

    wires_to_look_at = sorted([e for e in circuit.wires if e[0] == "x"], reverse=True)
    x = int(''.join([str(circuit.wires[e].get_value()) for e in wires_to_look_at]), 2)
    wires_to_look_at = sorted([e for e in circuit.wires if e[0] == "y"], reverse=True)
    y = int(''.join([str(circuit.wires[e].get_value()) for e in wires_to_look_at]), 2)
    print(x, y)

    #per hand in nem graphen gefunden
    possible = ["z06", "z11", "z16", "gfv", "hcm", "kfs", "tqm", "vwr"]

    perms = permutations(possible)
    p = []

    #print(parse_statements(instructions))
    target = x+y
    actual = 0
    solutions = set()
    for p in perms:
        #p = next(perms)
        pairs = dict()
        for i in range(0, 8, 2):
            pairs[p[i]] = p[i+1]
            pairs[p[i+1]] = p[i]
        circuit = Circuit()
        for i in instructions.split("\n"):
            circuit.add_instruction(i, pairs)
        for s in starting.split("\n"):
            name, value = s.split(": ")
            circuit.wires[name].set_signal(int(value))
        try:
            circuit.evaluate_all()
        except RecursionError as err:
            continue
        wires_to_look_at = sorted([e for e in circuit.wires if e[0] == "z"], reverse=True)
        actual = int(''.join([str(circuit.wires[e].get_value()) for e in wires_to_look_at]), 2)
        if actual == target:
            #print(target)
            solution = ','.join(sorted(p[:8]))
            if solution not in solutions:
                print(solution)
                solutions.add(solution)
            actual = 0
    wires_to_look_at = sorted([e for e in circuit.wires if e[0] == "z"], reverse=True)
    print(int(''.join([str(circuit.wires[e].get_value()) for e in wires_to_look_at]), 2))
    print(solutions)
