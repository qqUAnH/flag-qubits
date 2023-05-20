# TODO: Step1:replace each qubits in the original circuit to encoded block of quits
import cirq


class qubit_block:
    block_id = 0

    def __init__(self, qubit, stab_code):
        qubit_block.block_id += 1
        self.qubit = qubit
        self.stab_code = stab_code

    def qubits(self):
        cirq.LineQubit.range(len(self.stab_code))

class ft_measurement:

class ft_gate:
    def __init__(self, qubit_blocks, stab_code, gate:cirq.Gate):
        self.qubit_blocks = qubit_blocks
        self.stab_code = stab_code
        self.gate = gate

    def apply_gate(self):
        gates = []
        if len(self.qubit_blocks) == 1:
            for qubit in qubit_block[0]:
                gates.append(self.gate.on(qubit))
        elif len(self.qubit_blocks) == 2:
            pairs = zip(self.qubit_blocks[0], self.qubit_blocks[1])
            for pair in pairs:
                gates.append(self.gate.on(pair[0], pair[1]))
        return gates



def encode(circuit: cirq.Circuit, stab_code):
    qubit_blocks = []
    for qubit in circuit:
        qubit_blocks.append(qubit_block(qubit, stab_code))

# TODO: Step2: Replace
