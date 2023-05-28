# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

import cirq
import stim
import complier



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

class Flag:
    number_of_flag = 0
    def __init__(self):
        self.flag_qubitx = cirq.NamedQubit(str(self.number_of_flag) + "xf")
        self.flag_qubitz = cirq.NamedQubit(str(self.number_of_flag) + "zf")
        Flag.number_of_flag +=1
    def add_flag(self,op,only_include_x_flag = False, only_include_z_flag =False):
        op: cirq.Operation
        control = op.qubits[0]
        target  = op.qubits[1]
        flag_components = []
        if not only_include_z_flag :
            flag_components.append(cirq.CNOT(control, self.flag_qubitx))
        if not only_include_x_flag:
            flag_components.append(cirq.H(self.flag_qubitz))
            flag_components.append(cirq.CNOT(self.flag_qubitz, target))

        flag_components.append(op)

        if not only_include_z_flag :
            flag_components.append(cirq.CNOT(control, self.flag_qubitx))
            flag_components.append(cirq.measure(self.flag_qubitx))
        if not only_include_x_flag:
            flag_components.append(cirq.CNOT(self.flag_qubitz, target))
            flag_components.append(cirq.H(self.flag_qubitz))
            flag_components.append(cirq.measure(self.flag_qubitz))

        return flag_components








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    current_directory = os.getcwd()
    new_directory = '/path/to/new_directory'
    circuit = complier.test_circuit()
    icm_circuit = complier.decompose_to_ICM(circuit)
    icm_circuit: cirq.Circuit
    #TODO:need to only add flag between
    # add a big flag
    # operation with
    re =complier.generate_error_Circuit(circuit,2)
    for c in re:
        print("\n")
        print(c)







