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
    icm_circuit = c.decompose_to_ICM(circuit)
    icm_circuit: cirq.Circuit
    #TODO:need to only add flag between
    # add a big flag
    # operation with
    #why total case varies : fix number of total case
    x_error = error_circuit.X_error()

    pp = cirq.Circuit()
    q0 = cirq.NamedQubit("0")
    q1 = cirq.NamedQubit("1")
    fx0 = cirq.NamedQubit("0xf")
    pp.append(cirq.CNOT(q0,fx0))
    pp.append(cirq.CNOT(q0, q1))
    pp.append(cirq.CNOT(q0, fx0))
    pp.append(cirq.measure(fx0))

    #f_cir =c.add_flag(icm_circuit,number_of_x_flag=3,number_of_z_flag=3)
    print(icm_circuit)
    f_cir =c.add_flag(icm_circuit,stratergy="map")
    #f_cir =c.add_flag(icm_circuit,stratergy="heuristic")
    print("\n")
    print(f_cir)
    print("\n")
    #print("number_of_qubits="+str(len(f_cir.all_qubits())))
    Error_Map(icm_circuit).create_map_2(max_error=4)

    #test = []













