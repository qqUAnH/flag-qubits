
import numpy as np
import cirq
import stim
import stimcirq
import itertools
from functools import reduce
from src import circuit_preparation
from src.circuit_preparation import complier, error_circuit
from src.evaluation import state_vector_comparison

def evaluate_flag_circuit(flag_circuit, maximum_number_of_error):
    total_case = 0
    number_fail_case = 0
    number_success_case = 0
    number_of_fail_alarm = 0
    correct_state = state_vector_comparison.expected_state_vector(flag_circuit)
    test_kit = state_vector_comparison.possible_state_vector(flag_circuit, maximum_number_of_error)
    for number_of_error in range(maximum_number_of_error+1):
        #error_circuits = error_circuit.generate_input_error(flag_circuit, number_of_error)
        error_circuits = error_circuit.generate_error_circuit(flag_circuit, number_of_error)
        total_case = total_case + len(error_circuits)
        for cirq_circuit in error_circuits:
            print("\n")
            print(cirq_circuit[0])
            simulator = stim.TableauSimulator()
            stim_circuit = stimcirq.cirq_circuit_to_stim_circuit(cirq_circuit[1])
            simulator.do_circuit(stim_circuit)
            final_state = simulator.state_vector()
            flag_measurement = simulator.current_measurement_record()
            print(flag_measurement)
            if state_vector_comparison.have_error_propagated(final_state, test_kit):
                if True in flag_measurement:
                    number_success_case += 1
                    print("flags successfully catch error")
                else:
                    number_fail_case += 1
                    print("error propagated , but the flags fail to catch error")
            else:
                if True in flag_measurement:
                    number_of_fail_alarm += 1
                    print("Error didn't propagated , but the flag raise a fail alarm")
                else:
                    number_success_case += 1
                    print("Error didn't propagated ")
    print("total case" + str(total_case))
    print("number of time flag fail to catch error:"+str(number_fail_case))
    print("number of time flag successfully catch error:"+str(number_success_case))
    print("number of fail alarm:"+str(number_of_fail_alarm))
    print(state_vector_comparison.have_error_propagated(correct_state,test_kit))


