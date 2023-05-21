#=
test:
- Julia version: 
- Author: quan-hoang
- Date: 2023-05-19
=#
using Jabalizer
using PythonCall
cirq = pyimport("cirq");
gates_to_decomp = ["T", "T^-1"];
number_of_qubits = 3;
icm_input = Jabalizer.load_circuit_from_cirq_json("input_cirq_circuit.json")
(icm_circuit,_) = Jabalizer.compile(icm_input,number_of_qubits,gates_to_decomp)
Jabalizer.save_circuit_to_cirq_json(icm_circuit,"output_cirq_ICM_circuit.json");
cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")

print(cirq_circuit)



