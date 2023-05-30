
import cirq
from julia.api import Julia
import collections
from itertools import dropwhile


class Flag():
    number_of_flag = 0

    def __init__(self):
        self.flag_qubitx = cirq.NamedQubit(str(self.number_of_flag) + "xf")
        self.flag_qubitz = cirq.NamedQubit(str(self.number_of_flag) + "zf")
        Flag.number_of_flag += 1

    def create_flag(self, control, target):
        op: cirq.Operation
        x_flag = [[cirq.CNOT(control, self.flag_qubitx)],
                  [cirq.CNOT(control, self.flag_qubitx), cirq.measure(self.flag_qubitx)]
                  ]

        z_flag = [[cirq.H(self.flag_qubitz), cirq.CNOT(self.flag_qubitz, target)],
                  [cirq.CNOT(self.flag_qubitz, target), cirq.H(self.flag_qubitz), cirq.measure(self.flag_qubitz)]]
        return [x_flag, z_flag]





class Flag_complier():
    def keep_clifford_plus_T(self,op) -> bool:
        if isinstance(op.gate, (cirq.XPowGate,
                              cirq.YPowGate,
                              cirq.ZPowGate,
                              cirq.HPowGate,
                              cirq.CNotPowGate,
                              cirq.SwapPowGate
                              )):
            return True
    def test_circuit(self):
        q0 = cirq.NamedQubit('0')
        q1 = cirq.NamedQubit('1')
        circuit = cirq.Circuit()
        circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])
        return circuit

    def toffoli(self):
        qubits = [cirq.LineQubit(i) for i in range(3)]
        cirq_circuit = cirq.Circuit()
        cirq_circuit.append(cirq.CCNOT(*qubits))
        ct_circuit = cirq.Circuit(cirq.decompose(cirq_circuit, keep=self.keep_clifford_plus_T))

        return ct_circuit

    def single_gate(self):
        q0 = cirq.LineQubit(0)
        circuit = cirq.Circuit()
        circuit.append([cirq.H(q0), cirq.X(q0)])
        return circuit

    def decompose_to_ICM(self,circuit):
        json_string = cirq.to_json(cirq.Circuit(cirq.decompose(circuit, keep=self.keep_clifford_plus_T)))
        with open("../evaluate/input_cirq_circuit.json", "w") as outfile:
            outfile.write(json_string)
        #j = Julia(compiled_modules=False)
        #j.eval(open("/home/quan-hoang/PycharmProjects/flag-qubits/src/circuit_preparation/icm_converter.jl").read())
        cirq_circuit = cirq.read_json("../evaluate/output_cirq_ICM_circuit.json")
        return cirq_circuit
    def __is_moment_with_cnot__(self,momnet: cirq.Moment):
        for op in momnet.operations:
            if len(op.qubits) == 2:
                return True
        return False
    def add_flag(self,circuit: cirq.Circuit, number_of_flag: int, stratergy="random") -> cirq.Circuit:
        flag_circuit = cirq.Circuit()
        number_of_momnet = len(circuit.moments)
        moments_with_index = list(zip(circuit.moments, range(number_of_momnet)))
        moments_with_cnot_and_index = list(filter(lambda a: self.__is_moment_with_cnot__(a[0]), moments_with_index))


        control_qbits = []
        target_qbits = []
        x_end_moments = []
        z_end_moments = []

        if stratergy == "random":
            import random
            random_moments_with_cnot_and_index = random.choices( list(filter(lambda a: self.__is_moment_with_cnot__(a[0]), moments_with_index)) , k =number_of_flag)
            moments_with_cnot = list(map(lambda a: a[0], random_moments_with_cnot_and_index))
            # the first half of flags will be inserted before these moments
            index_start_moments = list(map(lambda a: a[1], random_moments_with_cnot_and_index))
            print(index_start_moments)
            # could be change here
            for i, m in zip(index_start_moments, moments_with_cnot):
                m:cirq.Moment
                # randomize end moment
                if i == number_of_momnet -1 :
                    x_end_moments.append(i)
                    z_end_moments.append(i)
                else:
                    x_end_moments.append(random.choice(range(i, number_of_momnet, 1)))
                    z_end_moments.append(random.choice(range(i, number_of_momnet, 1)))
                # since icm circuit have max one cnot a time:
                for op in m.operations:
                    print(op)
                    if len(list(op.qubits)) == 2:
                        control_qbits.append(op.qubits[0])
                        target_qbits.append(op.qubits[1])


            # TODO:ask professor if a flag must include x and z flag:
            x_flags = []
            z_flags = []

            # no z flag and there is more flag than needed
            for c, t in zip(control_qbits, target_qbits):
                print("a")
                print(c)
                print(t)
                f = Flag()
                x_flag, z_flag = f.create_flag(c, t)
                x_flags.append(x_flag)
                z_flags.append(z_flag)

            helper0x=0
            helper0z=0
            helper1x=0
            helper1z=0


            for index, current_moment in enumerate(circuit.moments):

                for n in range(number_of_flag):
                    #the problem is we already added the moments
                    if helper0x < number_of_flag and index_start_moments[n] == index:
                        for g in x_flags[helper0x][0]:
                            flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                        added_original_moment = True
                        helper0x += 1

                    if helper0z < number_of_flag and index_start_moments[n] == index:
                        for g in z_flags[helper0z][0]:
                            flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                        added_original_moment = True
                        helper0z +=1
                    #always append circuit in middle no matter what
                    flag_circuit.append(current_moment)

                    if helper1x < number_of_flag and x_end_moments[n] == index:
                        for g in x_flags[helper1x][1]:
                            flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                        added_original_moment = True
                        helper1x += 1

                    if helper1z < number_of_flag and z_end_moments[n] == index:
                        for g in z_flags[helper1z][1]:
                            flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                        added_original_moment = True
                        helper1z += 1

                    if helper1x > helper0x or helper1z > helper0z:
                        print("fail")



            return flag_circuit

        elif stratergy == "heuristic":
            raise NotImplemented



