
import numpy as np
import cirq
import stim
import stimcirq
import itertools
from functools import reduce
from src import circuit_preparation
from src.circuit_preparation import complier, error_circuit
from src.evaluation import state_vector_comparison

def evaluate_flag_circuit(flag_circuit, maximum_number_of_error, number_of_flag):
    total_case = 0
    number_of_flags = 0
    # flag return trivival but error propagated
    number_fail_case = 0
    # at least one flag return nontrivial
    number_success_case = 0
    #There could be a problem with my test-kit
    correct_state = state_vector_comparison.expected_state_vector(flag_circuit)
    test_kit = state_vector_comparison.possible_state_vector(flag_circuit, maximum_number_of_error)
    #why there are 12 combination ?
    print(len(test_kit))
    for number_of_error in range(maximum_number_of_error+1):
        #error_circuits = error_circuit.generate_input_error(flag_circuit, number_of_error)
        error_circuits = error_circuit.generate_random_error_Circuit(flag_circuit, number_of_error)
        total_case = total_case + len(error_circuits)
        for cirq_circuit in error_circuits:
            print(cirq_circuit)
            simulator = stim.TableauSimulator()
            stim_circuit = stimcirq.cirq_circuit_to_stim_circuit(cirq_circuit)
            simulator.do_circuit(stim_circuit)
            final_state = simulator.state_vector()
            flag_measurement = simulator.current_measurement_record()
            print(flag_measurement)
            if state_vector_comparison.have_error_propagated(final_state,test_kit):
                if False in flag_measurement:
                    number_fail_case +=1

                print("error propagate")
            else:
                if True in flag_measurement:
                    number_success_case +=1
                #TODO: can't dectect phase error
                print("trivial error")

    print("number of fail case:"+str(number_fail_case))
    print("number of success case:"+str(number_fail_case))
    print("total case"+str(total_case))

