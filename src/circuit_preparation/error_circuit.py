import cirq
import  itertools
from typing import List

#TODO:replace this with itertools


#TODO:A lot of refactoring  :(((
# create a class that represent error location and alows us to cancel out indentical error
class error_location():
    def __init__(self,qubit:cirq.NamedQubit,index:int):
        self.qubit = qubit
        self.index = index
#this is quite problem matric
def generate_error_string(number_of_error):
    errors = list(itertools.product('xz', repeat=number_of_error))

    return errors

def generate_all_error_location(circuit):
    re = []
    qubits = list( filter(lambda q:  not 'f' in q.name  ,circuit.all_qubits()))
    def is_moment_with_flag(m:cirq.Moment) :
        re = False
        for op in m.operations:
            op:cirq.Operation
            for q in op.qubits:
                q :cirq.NamedQubit
                if 'f' in q.name:
                    re = True
        return re
    for index, m in enumerate(circuit.moments):
        if not is_moment_with_flag(m):
            for q in qubits:
                re.append([q, index])
    return re

def create_error_moments(errors_string,location):
    def helper(error_char,qubit):
        if error_char == 'x':
            return cirq.Moment(cirq.X(qubit))
        elif error_char == 'z':
            return cirq.Moment(cirq.Z(qubit))
    return list(map(lambda a, b: helper(a, b[0]), errors_string, location))

#THis is a refactored function for create_error_moments:
def error_at_moments(errors_string,location:List[error_location]):
    def helper(error_char,qubit):
        if error_char == 'x':
            return cirq.Moment(cirq.X(qubit))
        elif error_char == 'z':
            return cirq.Moment(cirq.Z(qubit))
    return list(map(lambda a, b: helper(a, b.qubit), errors_string, location))


def generate_random_error_Circuit(circuit: cirq.Circuit, number_of_error: int):
    def add_error_moments(cir: cirq.Circuit, error_moments, location):
        # the varible location should be in the form (qubits,index)
        new_circuit = cirq.Circuit()
        for index , m in enumerate(cir.moments):
            for i, l in enumerate(location):
                if l[1] == index:
                   new_circuit.append(error_moments[i])
            new_circuit.append(m,strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        return new_circuit

    all_error_locations = generate_all_error_location(circuit)

    errors_string = generate_error_string(number_of_error)
    all_combination_of_error_location  = list(itertools.combinations_with_replacement(all_error_locations,number_of_error))
    all_error_circuit= []
    for e in errors_string:
        helper =map( lambda a : [create_error_moments(a[0],a[1]),a[1]]
            ,list(map( lambda l : [e,l] ,all_combination_of_error_location)))
        for i in helper:
            all_error_circuit.append(add_error_moments(circuit, i[0], i[1]))
    return all_error_circuit


def generate_input_error(circuit:cirq.Circuit,number_of_error:int, stratergy="all"):
    result = []
    qubits = list(filter(lambda q:  'f' not in q.name, circuit.all_qubits()))
    locations = list(map( lambda q: error_location(q, 0), qubits))
    combination_of_locations = list(itertools.combinations_with_replacement(list(locations), number_of_error))
    error_string = generate_error_string(number_of_error)

    #should replace this with map
    if stratergy == "all":
        for e in error_string:
            for cl in combination_of_locations:
                error_cir = cirq.Circuit()
                for m in error_at_moments(e,cl):
                    error_cir.append(m)
                result.append(error_cir+circuit)
    return result
















