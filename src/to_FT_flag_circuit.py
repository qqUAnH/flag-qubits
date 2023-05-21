# TODO: Step1:replace each qubits in the original circuit to encoded block of quits
import cirq


class qubit_block:
    block_id = 0
    #TODO:move qubits to init
    def __init__(self, qubits, stab_code):
        qubit_block.block_id += 1
        self.qubits = qubits
        self.stab_code = stab_code
        self.qubits = cirq.NamedQubit.range(len(stab_code), prefix=str(self.block_id))


class ft_measurement:
    pass

class ft_gate:
    def __init__(self, qubit_blocks, stab_code, gate:cirq.Gate):
        self.qubit_blocks = qubit_blocks
        self.stab_code = stab_code
        self.gate = gate

    def apply_gate(self):
        gates = []
        if len(self.qubit_blocks) == 1:
            for qubit in self.qubit_blocks[0].qubits:
                gates.append(self.gate.on(qubit))
        elif len(self.qubit_blocks) == 2:
            print(self.gate.num_qubits())

            pairs = zip(self.qubit_blocks[0].qubits, self.qubit_blocks[1].qubits)
            for pair in pairs:
                print(pair[0],pair[1])
                gates.append(self.gate.on(pair[0], pair[1]))
        return gates



def encode(circuit: cirq.Circuit, stab_code):
    qubit_blocks = []
    qubits = circuit.all_qubits()
    new_circuit =cirq.Circuit()
    for qubit in qubits:
        qubit_blocks.append(qubit_block(qubit, stab_code))
    qubit_blocks = list(zip(qubits, qubit_blocks))
    for q in qubit_blocks:
        print(q[0])



    for moment in circuit:
        moment: cirq.Moment
        for op in moment:
            op: cirq.Operation
            print(op.qubits)

            def is_op_target_to_encoded_qubit(q):
                if q in op.qubits:
                    return True
                else:
                    return False

            blocks = list( filter(lambda block:  is_op_target_to_encoded_qubit(block[0]), qubit_blocks))
            blocks = list(map(lambda item: item[1], blocks))
            ft_gates = ft_gate( blocks, stab_code,op.gate).apply_gate()
            new_circuit.append(ft_gates)
    for q in qubit_blocks :
        print(q[0])

    return  new_circuit

# TODO: Step2: Replace
