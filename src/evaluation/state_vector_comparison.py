
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
    flag_qubits = list(filter(lambda q: 'f'  in q.name,qubits))
    number_of_qubits = len(qubits)
    locations = list(itertools.combinations_with_replacement(range(number_of_qubits),number_of_error))

    del possible_error_string[0]
    for l in locations :
        for e in possible_error_string:
            helper = list(map(lambda n: identity_matrix ,range(number_of_qubits)))
            for index, error_char in zip(l, e) :
                q = qubits[index]
                q:cirq.NamedQubit
                if error_char == "x":
                    helper[index] = Pauli_x
                elif qubits[index] not in flag_qubits:
                    helper[index] = Pauli_z
            error_matrix = reduce(lambda a, b: np.kron(a, b), helper)
            result.append(np.dot(error_matrix, correct_state_vector))
    result.append(correct_state_vector)
    return result


def have_error_propagated(state_vector, possible_state_vectors):
    return not any(np.array_equal(state_vector, possible_vector) for possible_vector in possible_state_vectors)


