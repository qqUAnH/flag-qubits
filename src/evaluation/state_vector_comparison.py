
import numpy as np
import cirq
import stim
import stimcirq
import itertools
from functools import reduce
from src import circuit_preparation
from src.circuit_preparation import complier ,error_circuit


def expected_state_vector(circuit:cirq.Circuit):
    stim_circuit = stimcirq.cirq_circuit_to_stim_circuit(circuit)
    simulator = stim.TableauSimulator()
    simulator.do_circuit(stim_circuit)
    return simulator.state_vector()
#should do st that help me visualize
def possible_state_vector(circuit:cirq.Circuit,number_of_error:int):
    result = []
    identity_matrix = np.eye(2)
    Pauli_x=[[0,1],
              [1,0]]
    Pauli_z=[[1,0],
             [0,-1]]
    correct_state_vector = expected_state_vector(circuit)
    possible_error_string = []
    for n in range(number_of_error+1):
        possible_error_string += error_circuit.generate_error_string(n)
    print(possible_error_string)
    qubits = list(circuit.all_qubits())
    number_of_qubits = len(qubits)
    flag_qubits = list(filter(lambda q: 'f'  in q.name,qubits))
    original_qubits = list(filter(lambda q: 'f' not in q.name,qubits))
    locations = list(itertools.combinations_with_replacement(original_qubits,number_of_error))
    # can be changed
    for l in locations :
        for e in possible_error_string:
            helper = circuit.copy()
            for q, error_char in zip(l, e) :
                q:cirq.NamedQubit
                if error_char == "x":
                    helper.append(cirq.X(q))
                else:
                    helper.append(cirq.Z(q))
            simulator = stim.TableauSimulator()
            stim_circuit = stimcirq.cirq_circuit_to_stim_circuit(helper)
            simulator.do_circuit(stim_circuit)
            final_state = simulator.state_vector()
            result.append(final_state)
    print(len(result))
    result.append(correct_state_vector)
    return result


def have_error_propagated(state_vector, possible_state_vectors):
    return not any(np.array_equal(state_vector, possible_vector) for possible_vector in possible_state_vectors)


