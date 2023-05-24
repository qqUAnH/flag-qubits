
import cirq
from julia.api import Julia
import json
def keep_clifford_plus_T(op):
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
    circuit.append([cirq.H(q0), cirq.CNOT(q0, q1), cirq.T(q0)])
    return circuit

def toffoli():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    cirq_circuit = cirq.Circuit()
    cirq_circuit.append(cirq.CCNOT(*qubits))
    ct_circuit = cirq.Circuit(cirq.decompose(cirq_circuit, keep=keep_clifford_plus_T))
    cirq_circuit.append(cirq.measure(qubits))
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
    #j.eval('include("jabba.jl")')
    cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")
    return cirq_circuit





