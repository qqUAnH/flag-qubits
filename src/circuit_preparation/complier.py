
import cirq
from julia.api import Julia
import collections
from itertools import dropwhile
from error_map import Error_Map


class Flag():
    number_of_flag = 0

    def __init__(self):
        self.flag_qubitx = cirq.NamedQubit(str(self.number_of_flag) + "xf")
        self.flag_qubitz = cirq.NamedQubit(str(self.number_of_flag) + "zf")
        Flag.number_of_flag += 1

    def create_x_flag(self, control):
        x_flag = [[cirq.CNOT(control, self.flag_qubitx)],
                  [cirq.CNOT(control, self.flag_qubitx), cirq.measure(self.flag_qubitx),
                   cirq.ResetChannel().on(self.flag_qubitx)]
                  ]
        return x_flag
    #fix bug her
    def create_z_flag(self, target):
        z_flag = [[cirq.H(self.flag_qubitz), cirq.CNOT(self.flag_qubitz, target)],
                  [cirq.CNOT(self.flag_qubitz, target), cirq.H(self.flag_qubitz), cirq.measure(self.flag_qubitz),
                   cirq.ResetChannel().on(self.flag_qubitz)]]
        return z_flag






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
        q0,q1,q2,q3 = [cirq.LineQubit(i) for i in range(4)]
        circuit = cirq.Circuit()
        circuit.append(cirq.T(q1))
        circuit.append( cirq.CNOT(q0, q2))
        circuit.append(cirq.CNOT(q0, q2))
        circuit.append(cirq.CNOT(q3, q1))


        print(circuit)

        return circuit

    def toffoli(self):
        qubits = [cirq.LineQubit(i) for i in range(3)]
        cirq_circuit = cirq.Circuit()
        cirq_circuit.append(cirq.CCNOT(*qubits))
        ct_circuit = cirq.Circuit(cirq.decompose(cirq_circuit, keep=self.keep_clifford_plus_T))

        return ct_circuit

    def powerpoint_circuit(self):
        circuit = cirq.Circuit()
        q0, q1 = [cirq.LineQubit(i) for i in range(2)]
        circuit.append(cirq.CNOT(q0, q1))
        return circuit

    def test_circuit2(self):
        qf , q1 ,q2 ,q3 = [cirq.LineQubit(i) for i in range(4)]
        circuit = cirq.Circuit()
        circuit.append([ cirq.H(q3),cirq.CNOT(q1,q2)])
        circuit.append(cirq.CNOT(q1,q3))
        circuit.append(cirq.CNOT(q1,q2))

        return circuit

    def decompose_to_ICM(self,circuit):
        json_string = cirq.to_json(cirq.Circuit(cirq.decompose(circuit, keep=self.keep_clifford_plus_T)))
        with open("input_cirq_circuit.json", "w") as outfile:
            outfile.write(json_string)
        cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")
        return cirq_circuit
    def __is_moment_with_cnot__(self,momnet: cirq.Moment):
        for op in momnet.operations:
            if len(op.qubits) == 2:
                return True
        return False
    def add_flag(self,circuit: cirq.Circuit, number_of_x_flag=0, number_of_z_flag=0, stratergy="random") -> cirq.Circuit:
        # setup
        flag_circuit = cirq.Circuit()
        number_of_momnet = len(circuit.moments)
        moments_with_index = list(zip(circuit.moments, range(number_of_momnet)))
        moments_with_cnot_and_index = list(filter(lambda a: self.__is_moment_with_cnot__(a[0]), moments_with_index))
        control_qbits = []
        target_qbits = []
        x_start_moments = []
        z_start_moments = []
        x_end_moments = []
        z_end_moments = []


        if stratergy == "random":
            import random
            def random_moments_with_cnot_and_index(number_of_flag):
                return list(random.choices(list(filter(lambda a: self.__is_moment_with_cnot__(a[0]), moments_with_index)) , k =number_of_flag))
            x_random_moments_with_cnot = random_moments_with_cnot_and_index(number_of_x_flag)
            z_random_moments_with_cnot = random_moments_with_cnot_and_index(number_of_z_flag)

            x_start_moments = list(map(lambda a: a[1], x_random_moments_with_cnot))
            z_start_moments = list(map(lambda a: a[1], z_random_moments_with_cnot))
            z_random_moments_with_cnot = list(map(lambda a: a[0], z_random_moments_with_cnot))
            x_random_moments_with_cnot = list(map(lambda a: a[0], x_random_moments_with_cnot))

            for x,mx in zip(x_start_moments, x_random_moments_with_cnot):
                m:cirq.Moment
                if x == number_of_momnet -1 :
                    x_end_moments.append(x)
                else:
                    x_end_moments.append(random.choice(range(x, number_of_momnet, 1)))

                for op in mx.operations:
                    if len(list(op.qubits)) == 2:
                        control_qbits.append(op.qubits[0])

            for z, mz in zip(z_start_moments, z_random_moments_with_cnot):
                m: cirq.Moment
                if z == number_of_momnet - 1:
                    z_end_moments.append(z)
                else:
                    z_end_moments.append(random.choice(range(z, number_of_momnet, 1)))
                for op in mz.operations:
                    if len(list(op.qubits)) == 2:
                        target_qbits.append(op.qubits[1])
        elif stratergy == "heuristic":
            #Brute force:D or i could do it better?
            for qubits in circuit.all_qubits():
                x_gatherer = []
                z_gatherer = []
                for moment,index in moments_with_cnot_and_index:
                    moment:cirq.Moment
                    if moment.operations[0].qubits[0] == qubits:
                        x_gatherer.append(index)
                        if len(z_gatherer) >= 2:
                            z_start_moments.append(z_gatherer[0])
                            z_end_moments.append(z_gatherer[-1])
                            target_qbits.append(qubits)
                        z_gatherer = []
                    elif moment.operations[0].qubits[1] == qubits:
                        z_gatherer.append(index)
                        if len(x_gatherer) >= 2:
                            x_start_moments.append(x_gatherer[0])
                            x_end_moments.append(x_gatherer[-1])
                            control_qbits.append(qubits)
                        x_gatherer = []
                if len(x_gatherer) >= 2:
                    x_start_moments.append(x_gatherer[0])
                    x_end_moments.append(x_gatherer[-1])
                    control_qbits.append(qubits)
                if len(z_gatherer) >= 2:
                    z_start_moments.append(z_gatherer[0])
                    z_end_moments.append(z_gatherer[-1])
                    target_qbits.append(qubits)
        elif stratergy == "map":
            helper =moments_with_cnot_and_index[0][1]
            x_map, z_map = Error_Map(circuit).create_map()
            control_qbits = [key[0] for key, value in x_map.items() if len(value) > 1]
            target_qbits  = [key[0] for key, value in z_map.items() if len(value) > 1]
            x_start_moments = list(map(lambda a:0,control_qbits))
            z_start_moments = list(map(lambda a:0,target_qbits))
            x_end_moments = [(key[1]+helper) for key, value in x_map.items() if len(value) > 1]
            z_end_moments = [(key[1]+helper) for key, value in z_map.items() if len(value) > 1]
            print(control_qbits)
            print(x_end_moments)
        x_flags = []
        z_flags = []
        for control in control_qbits:
            f = Flag()
            x_flags.append(f.create_x_flag(control))
        for target in target_qbits:
            f = Flag()
            z_flags.append(f.create_z_flag(target))
        helper0x = 0
        helper0z = 0
        helper1x = 0
        helper1z = 0
        #
        number_of_x_flag = len(x_start_moments)
        #number_of_z_flag = len(z_start_moments)
        for index, current_moment in enumerate(circuit.moments):
            for n in range(number_of_x_flag):
                if helper0x < number_of_x_flag and x_start_moments[n] == index:
                    for g in x_flags[helper0x][0]:
                        flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                    helper0x += 1

            for n in range(number_of_z_flag):
                if helper0z < number_of_z_flag and z_start_moments[n] == index:
                    for g in z_flags[helper0z][0]:
                        flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                    helper0z += 1

            flag_circuit.append(current_moment)

            for n in range(number_of_x_flag):
                if helper1x < number_of_x_flag and x_end_moments[n] == index:
                    print(index)
                    for g in x_flags[helper1x][1]:
                        flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                    helper1x += 1
                    print(flag_circuit)

            for n in range(number_of_z_flag):
                if helper1z < number_of_z_flag and z_end_moments[n] == index:
                    for g in z_flags[helper1z][1]:
                        flag_circuit.append(g, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                    helper1z += 1

        return flag_circuit





