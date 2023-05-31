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






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c = complier.Flag_complier()
    current_directory = os.getcwd()
    new_directory = '/path/to/new_directory'
    circuit = c.toffoli()
    icm_circuit = c.decompose_to_ICM(circuit)
    icm_circuit: cirq.Circuit
    #TODO:need to only add flag between
    # add a big flag
    # operation with
    f_cir =c.add_flag(c.test_circuit(),1)
    print(f_cir)

    evaluate.evaluate_flag_circuit(f_cir,1,0)









