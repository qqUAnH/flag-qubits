# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.




# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

import cirq
import stim
import stimcirq
from src import circuit_preparation
from src.circuit_preparation import complier ,error_circuit
from src.evaluation import evaluate
from error_map import Error_Map







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c = complier.Flag_complier()
    current_directory = os.getcwd()
    new_directory = '/path/to/new_directory'
    circuit = c.test_circuit()



    x_error = error_circuit.X_error()
    qubits  = [cirq.LineQubit(i) for i in range(5)]
    circuitA = cirq.testing.random_circuit(qubits,n_moments=5,op_density=0.6,gate_domain={cirq.CNOT:2})
    circuit = cirq.testing.random_circuit(qubits,n_moments=1,op_density=0.7,gate_domain={cirq.H:1}) + circuitA
    print(circuit)
    icm_circuit = c.decompose_to_ICM(circuit)
    icm_circuit: cirq.Circuit

    pp = cirq.Circuit()
    q0 = cirq.NamedQubit("0")
    q1 = cirq.NamedQubit("1")
    fx0 = cirq.NamedQubit("0xf")
    pp.append(cirq.X(q0))
    pp.append(cirq.CNOT(q0,fx0))
    pp.append(cirq.CNOT(q0, q1))
    pp.append(cirq.CNOT(q0, fx0))
    pp.append(cirq.measure(fx0))

    icm_circuit = c.decompose_to_ICM(c.test_circuit2())

    #f_cir =c.add_flag(icm_circuit,number_of_x_flag=3,number_of_z_flag=3)
    f_cir =c.add_flag(icm_circuit,stratergy="map")
    #f_cir =c.add_flag(icm_circuit,stratergy="heuristic")
    print("\n")
    print(f_cir)
    print("\n")


    for i in [1,2]:
        evaluate.evaluate_flag_circuit(f_cir,maximum_number_of_error=i)

    #test = []













