
import cirq
from julia.api import Julia
import collections
def keep_clifford_plus_T(op) -> bool:
    if isinstance(op.gate, (cirq.XPowGate,
                          cirq.YPowGate,
                          cirq.ZPowGate,
                          cirq.HPowGate,
                          cirq.CNotPowGate,
                          cirq.SwapPowGate
                          )):
        return True
def test_circuit():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])
    return circuit

def toffoli():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    cirq_circuit = cirq.Circuit()
    cirq_circuit.append(cirq.CCNOT(*qubits))
    ct_circuit = cirq.Circuit(cirq.decompose(cirq_circuit, keep=keep_clifford_plus_T))

    return ct_circuit

def single_gate():
    q0 = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q0), cirq.X(q0)])
    return circuit

def decompose_to_ICM(circuit):
    json_string = cirq.to_json(circuit)
    with open("input_cirq_circuit.json", "w") as outfile:
        outfile.write(json_string)
    #j = Julia(compiled_modules=False)
    #j.eval(open("/home/quan-hoang/PycharmProjects/flag-qubits/src/circuit_preparation/icm_converter.jl").read())
    cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")
    return cirq_circuit

class Flag:
    number_of_flag = 0
    def __init__(self):
        self.flag_qubitx = cirq.NamedQubit(str(self.number_of_flag) + "xf")
        self.flag_qubitz = cirq.NamedQubit(str(self.number_of_flag) + "zf")
        Flag.number_of_flag +=1
    def create_flag(self,op,only_include_x_flag = False, only_include_z_flag =False):
        op: cirq.Operation
        control = op.qubits[0]
        target  = op.qubits[1]
        #inclue two moment
        x_flag = [cirq.Moment(cirq.CNOT(control, self.flag_qubitx)),
                  cirq.Moment(cirq.CNOT(control, self.flag_qubitx),cirq.measure(self.flag_qubitx))]

        z_flag = [cirq.Moment(cirq.H(self.flag_qubitz),cirq.CNOT(self.flag_qubitz, target)),
                  cirq.Moment(cirq.CNOT(self.flag_qubitz, target),cirq.H(self.flag_qubitz),cirq.measure(self.flag_qubitz))]
        return [x_flag,z_flag]


def is_moment_with_cnot(momnet: cirq.Moment):
    for op in momnet.operations:
        if len(op.qubits) == 2:
        return True
    return False

def add_flag(circuit: cirq.Circuit, number_of_flag: int, stratergy = "random") -> cirq.Circuit:
    flag_circuit = cirq.Circuit()
    if stratergy == "random":
        import random
        return flag_circuit
    elif stratergy == "heuristic":



def generate_error_Circuit(circuit: cirq.Circuit, number_of_error: int):
    import  itertools
    def generate_error():
        error = []
        generate_error_helper('', number_of_error, strings)
        return error
    def generate_error_helper(current_string, n, strings):
        if len(current_string) == n:
            strings.append(current_string)
        else:
            generate_error_helper(current_string + 'x', n, strings)
            generate_error_helper(current_string + 'z', n, strings)
    def create_error_moments(errors_string,location)
        def helper(error_char,qubit):
            if error_char == 'x':
                return cirq.Moment(cirq.X(qubit))
            elif error_char == 'z':
                return cirq.Moment(cirq.Z(qubit))

        return list(map(  lambda e, l: helper(e,l[0]) ,list(zip(errors_string,location))))

    def add_error_moments(cir: cirq.Circuit, error_moments, location):
        # the varible location should be in the form (qubits,momment)
        new_circuit = cirq.Circuit()

        i = 0
        for m in cir.moments:
            if m == location[i][1]:
                new_circuit.append(error_moments[i])
                new_circuit.append(m)
                i += 1
            else:
                new_circuit.append(m)
        return new_circuit

    qubits  =circuit.all_qubits()
    moments =circuit.moments
    all_error_locations = list(zip(qubits,moments))
    errors_string = generate_error()
    all_combination_of_error_location  = itertools.combinations_with_replacement(all_error_locations,number_of_error)
    all_error_circuit= []
    for e in errors_string:
        helper =map( lambda a : [create_error_moments(a[0],a[1]),a[1]]
            ,list(map( lambda l : [e,l] ,all_combination_of_error_location)))
        for i in helper:
            all_error_circuit.append(add_error_moments(circuit,i[0],i[1]))
    return all_error_circuit





