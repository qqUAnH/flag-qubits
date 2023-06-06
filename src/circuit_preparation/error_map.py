import cirq
from concurrent.futures import ThreadPoolExecutor
from functools import reduce

class Error_Map():
    def __is_moment_with_cnot__(self,momnet: cirq.Moment):
        for op in momnet.operations:
            if len(op.qubits) == 2:
                return True
        return False
    def __init__(self,circuit:cirq.Circuit):
        self.circuit = circuit
        self.moment_with_cnot = list(filter(lambda m: self.__is_moment_with_cnot__(m),list(circuit.moments)))
        self.qubits = list(circuit.all_qubits())
        self.map_size = len(self.moment_with_cnot)
        self.X_map = {}
        self.Z_map = {}

    def create_map(self):
        #THere is a problem with index
        self.moment_with_cnot.reverse()
        for i,moment in enumerate(self.moment_with_cnot):
            index = self.map_size-i-1
            moment:cirq.Moment
            control, target = moment.operations[0].qubits
            for qubit in self.qubits:
                qubit:cirq.NamedQubit
                control:cirq.NamedQubit
                target:cirq.NamedQubit
                original_error = (qubit , index)
                propagated_x_error = [(qubit,index+1)]
                propagated_z_error = [(qubit,index+1)]

                if control == qubit:
                    propagated_x_error.append((target,index+1))
                elif target == qubit:
                    propagated_z_error.append((control,index+1))

                # we will query the dictionary to get the results
                helper1 = propagated_x_error
                helper2 = propagated_z_error
                if not index+1 == self.map_size:
                    propagated_x_error = []
                    propagated_z_error =[]
                    for i,error in enumerate(helper1):
                        for e in self.X_map[tuple(error)]:
                            propagated_x_error.append(e)
                    for i,error in enumerate(propagated_z_error):
                        for e in self.Z_map[tuple(error)]:
                            propagated_z_error.append(e)


                propagated_x_error = [e for e in propagated_x_error if propagated_x_error.count(e) % 2 == 1]
                propagated_z_error = [e for e in propagated_z_error if propagated_z_error.count(e) % 2 == 1]

                self.X_map[tuple(original_error)] = propagated_x_error
                self.Z_map[tuple(original_error)] = propagated_z_error
            print("")
            print("current map:")
            for key,val in self.X_map.items():
                print(key[1],val)
        return [self.X_map,self.Z_map]




