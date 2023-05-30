# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

import cirq
import stim
import stimcirq
from src import circuit_preparation
from src.circuit_preparation import complier





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
    def evaluate(cir,time):
        def get_correct_stabilizer_state():
            simulator = stim.TableauSimulator()
            simulator.do_circuit(stimcirq.cirq_circuit_to_stim_circuit(cir))
            print(simulator.state_vector() )
            simulator.h(1)
            print(simulator.current_inverse_tableau())
            return simulator.canonical_stabilizers()[0]
        def sampleing():
            for error_circuit in c.generate_error_Circuit(cir,1):
                simulator = stim.TableauSimulator()
                flag_circuit = c.add_flag(icm_circuit, 2)
                stim_circuit = stimcirq.cirq_circuit_to_stim_circuit(flag_circuit)
                simulator.do_circuit(stim_circuit)

                return simulator.canonical_stabilizers()
        get_correct_stabilizer_state()
    print(c.test_circuit())
    f = c.add_flag(c.test_circuit(),1)
    print(f)
    for i in range(2):
        f = c.add_flag(icm_circuit, 2)
        print(f)








