#=
test:
- Julia version: 
- Author: quan-hoang
- Date: 2023-05-19
=#

using Jabalizer
using PythonCall
cirq = pyimport("cirq");

circuit_file_name = "input_cirq_circuit.json"
gates_to_decomp = ["T", "T^-1"];
icm_input = Jabalizer.load_circuit_from_cirq_json(circuit_file_name)
(icm_circuit, _) = Jabalizer.compile(icm_input, gates_to_decomp)
Jabalizer.save_circuit_to_cirq_json(icm_circuit, "output_cirq_ICM_circuit.json");



