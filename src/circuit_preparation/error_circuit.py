import cirq
import  itertools
from typing import List
import numpy as np




class X_error(cirq.Gate):
    def __init__(self):
        super().__init__()
    def num_qubits(self) -> int:
        return 1
    def _circuit_diagram_info_(self, args):
        return "x_error"

    def _unitary_(self):
        return np.array([
            [0,1],
            [1,0]
        ])

    def validate_args(self,qubit):
        pass


class Z_error(cirq.Gate):
    def __init__(self):
        super().__init__()
    def num_qubits(self) -> int:
        return 1
    def _circuit_diagram_info_(self, args):
        return "z_error"

    def _unitary_(self):
        return np.array([
            [1,0],
            [0,-1]
        ])

    def validate_args(self,qubit):
        pass

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

#THis is a refactored function for create_error_moments:
def error_at_moments(errors_string,location:List[error_location]):
    def helper(error_char,qubit):
        if error_char == 'x':
            x_error_gate = X_error()
            x_error_op = x_error_gate.on(qubit)
            moment = cirq.Moment(x_error_op)
            return moment
        elif error_char == 'z':
            z_error_gate = Z_error()
            z_error_op = z_error_gate.on(qubit)
            moment = cirq.Moment(z_error_op)
            return moment
    def helper2(error_char,qubit):
        if error_char == 'x':
            x_error_gate = cirq.X
            x_error_op = x_error_gate.on(qubit)
            moment = cirq.Moment(x_error_op)
            return moment
        elif error_char == 'z':
            z_error_gate = cirq.Z
            z_error_op = z_error_gate.on(qubit)
            moment = cirq.Moment(z_error_op)
            return moment
    return [list(map(lambda a, b: helper(a, b.qubit), errors_string, location)), list(map(lambda a, b: helper2(a, b.qubit), errors_string, location))]



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
                # ERROR_CIR AND ERROR CI2 IS basically the same
                error_cir = cirq.Circuit()
                error_cir2 = cirq.Circuit()
                error1, error2 =error_at_moments(e,cl)
                for m in error1:
                    error_cir.append(m)
                for m in error2:
                    error_cir2.append(m)

                result.append([error_cir+circuit, error_cir2+circuit])
    return result



def generate_error_circuit(circuit:cirq.Circuit,number_of_error:int):
    result = []
    moments = list(circuit.moments)
    for i in range(len(moments)):
        #we divide the moment into two part
        first_part = moments[:i]
        second_part = moments[-len(moments)+i:]

        circuit1 = cirq.Circuit()
        circuit1.append(first_part)

        circuit2 = cirq.Circuit()
        circuit2.append(second_part)
        circuit2 = generate_input_error(circuit2,number_of_error)

        for c in circuit2:
            result.append([circuit1+c[0],circuit1+c[1]])
    return result













