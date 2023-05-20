
import cirq
import julia

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
    circuit.append([cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1)])
    return circuit

def decompose_to_ICM(circuit):
    json_string = cirq.to_json(circuit)

    with open("input_cirq_circuit.json", "w") as outfile:
        outfile.write(json_string)
    j = julia.Julia()
    j.include("jabba.jl")

    cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")
    print(cirq_circuit)





