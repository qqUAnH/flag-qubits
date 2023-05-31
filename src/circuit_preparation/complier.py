
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
    #
    def test_circuit(self):
        q0 = cirq.NamedQubit('0')
        q1 = cirq.NamedQubit('1')
        q2 = cirq.NamedQubit('2')
        circuit = cirq.Circuit()
        circuit.append( cirq.CNOT(q0, q1))
        circuit.append(cirq.CNOT(q1, q2))
        print("this circuit should have 10 place where error can propagate")
        print(circuit)
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
        with open("input_cirq_circuit.json", "w") as outfile:
            outfile.write(json_string)
        #j = Julia(compiled_modules=False)
        #j.eval(open("/home/quan-hoang/PycharmProjects/flag-qubits/src/circuit_preparation/icm_converter.jl").read())
        cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")
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
        x_start_moments = []
        x_end_momemts = []
        x_end_moments = []
        z_end_moments = []

        if stratergy == "random":
            import random
            def random_moments_with_cnot_and_index():

                return list(random.choices(list(filter(lambda a: self.__is_moment_with_cnot__(a[0]), moments_with_index)) , k =number_of_flag))
            x_random_moments_with_cnot = random_moments_with_cnot_and_index()
            z_random_moments_with_cnot = random_moments_with_cnot_and_index()

            x_start_moments = list(map(lambda a: a[1], x_random_moments_with_cnot))
            z_start_moments = list(map(lambda a: a[1], z_random_moments_with_cnot))
            z_random_moments_with_cnot = list(map(lambda a: a[0], z_random_moments_with_cnot))
            x_random_moments_with_cnot = list(map(lambda a: a[0], x_random_moments_with_cnot))
            # the first half of flags will be inserted before these moments
            # could be change here
            for x,z,mx,mz in zip(x_start_moments,z_start_moments, x_random_moments_with_cnot,z_random_moments_with_cnot):
                m:cirq.Moment
                print(x)
                print(z)
                print(mx)
                print(mz)
                # randomize end moment
                if x == number_of_momnet -1 :
                    x_end_moments.append(x)
                else:
                    x_end_moments.append(random.choice(range(x, number_of_momnet, 1)))
                if z == number_of_momnet -1 :
                    z_end_moments.append(z)
                else:
                    z_end_moments.append(random.choice(range(z, number_of_momnet, 1)))

                for op in mx.operations:
                    if len(list(op.qubits)) == 2:
                        control_qbits.append(op.qubits[0])
                        target_qbits.append(op.qubits[1])
                for op in mz.operations:
                    if len(list(op.qubits)) == 2:
                        control_qbits.append(op.qubits[0])
                        target_qbits.append(op.qubits[1])

            # TODO:ask professor if a flag must include x and z flag:
            x_flags = []
            z_flags = []

            # no z flag and there is more flag than needed
            for c, t in zip(control_qbits, target_qbits):

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
                    if helper0x < number_of_flag and x_start_moments[n] == index:
                        for g in x_flags[helper0x][0]:
                            flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                        added_original_moment = True
                        helper0x += 1

                    if helper0z < number_of_flag and z_start_moments[n] == index:
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



