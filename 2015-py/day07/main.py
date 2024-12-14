import os

import dotenv
import requests
from kryptikkaocutils.Input import write_input_to_file

class Wire:
    def __init__(self, name):
        self.name = name
        self.signal = None # Will hold the evaluated value
        self.operation = None  # Holds the operation that computes this wire's value

    def get_value(self):
        """Evaluate and cache the wire's value if not already set."""
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
        elif self.operator == "LSHIFT":
            return left_value << right_value
        elif self.operator == "RSHIFT":
            return left_value >> right_value
        raise ValueError(f"Unknown binary operator: {self.operator}")


class Circuit:
    def __init__(self):
        self.wires = {}

    def get_wire(self, name):
        """Retrieve or create a wire."""
        if name not in self.wires:
            self.wires[name] = Wire(name)
        return self.wires[name]

    def add_instruction(self, instruction):
        """Parse and add an instruction to the circuit."""
        parts = instruction.strip().split(" -> ")
        expression, target_name = parts[0], parts[1]
        target_wire = self.get_wire(target_name)

        if expression.isdigit():  # Direct value assignment
            target_wire.signal = int(expression)
            return
        elif expression.isalpha():  # Direct wire-to-wire assignment
            source_wire = self.get_wire(expression)
            target_wire.operation = UnaryOperation("ASSIGN", source_wire, target_wire)
        elif "NOT" in expression:  # Unary NOT operation
            operand_name = expression.split("NOT ")[1]
            operand_wire = self.get_wire(operand_name)
            target_wire.operation = UnaryOperation("NOT", operand_wire, target_wire)
        else:  # Binary operation
            for operator in ["AND", "OR", "LSHIFT", "RSHIFT"]:
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
        """Get the value of a specific wire."""
        wire = self.get_wire(wire_name)
        return wire.get_value()

    def evaluate_all(self):
        """Evaluate all wires and return their values."""
        return {name: wire.get_value() for name, wire in self.wires.items()}

def part1(circuit):
    print(circuit.evaluate("a"))


def part2(inputs):
    print(circuit.evaluate("a"))




def gen_wires(inputs):
    circuit = Circuit()
    for i in inputs:
        circuit.add_instruction(i)
    return circuit


if __name__ == "__main__":
    fname = "i.txt"
    if not os.path.isfile(fname):
        write_input_to_file(2015, 7, fname)
    inputs = open(fname).readlines()
    circuit = gen_wires(inputs)
    #part1(circuit)
    part2(inputs)