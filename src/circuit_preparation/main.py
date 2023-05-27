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
    def cnot_to_flag(self,control):
        return [cirq.CZ(self.flag_qubitz,control),cirq.CNOT(control,self.flag_qubitx)]

    def add_x_flag(self,op):
        op:cirq.Operation
        control = op.qubits[0]
        flag_components = []
        flag_components.append(cirq.CNOT(control,self.flag_qubitx))
        flag_components.append(op)
        flag_components.append(cirq.CNOT(control,self.flag_qubitx))
        flag_components.append(cirq.measure(self.flag_qubitx))
        return flag_components
    def add_z_flag(self,op):
        op: cirq.Operation
        target = op.qubits[1]
        flag_components = []
        flag_components.append(cirq.H(self.flag_qubitz))
        flag_components.append(cirq.CNOT( self.flag_qubitz,target))
        flag_components.append(op)
        flag_components.append(cirq.CNOT( self.flag_qubitz,target))
        flag_components.append(cirq.H(self.flag_qubitz))
        flag_components.append(cirq.measure(self.flag_qubitz))
        return flag_components
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
    def add_flag(circuit: cirq.Circuit, number_of_flag: int, stratergy = "random") -> cirq.Circuit:
        flag_circuit = cirq.Circuit()
        if stratergy == "random":
            import random
            # a helper function to filter out moment that have Cnot
            def is_moment_with_cnot(momnet:cirq.Moment):
                for op in momnet.operations:
                    if len(op.qubits) == 2:
                        return True
                return False
            # a helper function that random a number_of_flag in list of moment_with_cnot:
            def randomize_targets(moments):
                return random.choices(moments, weights=None, cum_weights=None, k=number_of_flag)
            # a helper_function to check if a flag should be added to a momment:
            def should_add_flag(moment,randomized_targets):
                for target in randomized_targets:
                    if target == moment:
                        return True
                return False

            momments_with_cnot = list( filter(lambda m: is_moment_with_cnot(m),circuit.moments))
            targets = randomize_targets(momments_with_cnot)

            for m in circuit.moments:
                m:cirq.Moment
                operations = m.operations
                gate = []
                for op in operations:
                    op:cirq.Operation
                    if len(op.qubits) == 2 and should_add_flag(m,targets):
                        for g in Flag().add_flag(op):
                            gate.append(g)
                    else:
                        gate.append(op)
                flag_circuit.append(gate, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
            return flag_circuit
        elif stratergy == "heuristic":
            raise NotImplemented
    flag_cir = add_flag(icm_circuit,number_of_flag=2)
    print(icm_circuit)
    print("\n")
    print(flag_cir)





