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
    f_cir =c.add_flag(icm_circuit,stratergy="map")
    #f_cir =c.add_flag(icm_circuit,stratergy="heuristic")
    print(f_cir)
    #WHy the fuck did the result vary ?
    print("number_of_qubits="+str(len(f_cir.all_qubits())))
    evaluate.evaluate_flag_circuit(f_cir,2)












