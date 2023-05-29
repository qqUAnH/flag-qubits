
import cirq
from julia.api import Julia
import collections
from itertools import dropwhile
def keep_clifford_plus_T(op) -> bool:
    if isinstance(op.gate, (cirq.XPowGate,
                          cirq.YPowGate,
                          cirq.ZPowGate,
                          cirq.HPowGate,
                          cirq.CNotPowGate,
                          cirq.SwapPowGate
                          )):
        return True
def test_circuit():
    q0 = cirq.NamedQubit('0')
    q1 = cirq.NamedQubit('1')
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])
    return circuit

def toffoli():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    cirq_circuit = cirq.Circuit()
    cirq_circuit.append(cirq.CCNOT(*qubits))
    ct_circuit = cirq.Circuit(cirq.decompose(cirq_circuit, keep=keep_clifford_plus_T))

    return ct_circuit

def single_gate():
    q0 = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q0), cirq.X(q0)])
    return circuit

def decompose_to_ICM(circuit):
    json_string = cirq.to_json(cirq.Circuit(cirq.decompose(circuit, keep=keep_clifford_plus_T)))
    with open("input_cirq_circuit.json", "w") as outfile:
        outfile.write(json_string)
    #j = Julia(compiled_modules=False)
    #j.eval(open("/home/quan-hoang/PycharmProjects/flag-qubits/src/circuit_preparation/icm_converter.jl").read())
    cirq_circuit = cirq.read_json("output_cirq_ICM_circuit.json")
    return cirq_circuit

class Flag():
    number_of_flag = 0
    def __init__(self):
        self.flag_qubitx = cirq.NamedQubit(str(self.number_of_flag) + "xf")
        self.flag_qubitz = cirq.NamedQubit(str(self.number_of_flag) + "zf")
        Flag.number_of_flag += 1
    def create_flag(self,control,target):
        op: cirq.Operation
        x_flag = [[cirq.CNOT(control, self.flag_qubitx)],
                  [cirq.CNOT(control, self.flag_qubitx), cirq.measure(self.flag_qubitx)]
                  ]

        z_flag = [[cirq.H(self.flag_qubitz), cirq.CNOT(self.flag_qubitz, target)],
                  [cirq.CNOT(self.flag_qubitz, target), cirq.H(self.flag_qubitz), cirq.measure(self.flag_qubitz)]]
        return [x_flag, z_flag]


#brute force fucntion that generate error


def add_flag(circuit: cirq.Circuit, number_of_flag: int, stratergy = "random") -> cirq.Circuit:
    flag_circuit = cirq.Circuit()
    if stratergy == "random":
        import random
        #fix this tommorw
        number_of_momnet = len(circuit.moments)
        start_moments = random.choices( range(number_of_momnet), k=number_of_flag)

        qubits = list(map(lambda a: random.choice(list(circuit.all_qubits())), [0]+ list(range(1,number_of_flag,1))))
        #this is the problem
        end_moments = []
        for m in start_moments:
            start_index= m
            if m == number_of_momnet-1:
                end_moments.append(m)
            else:
                end_moments.append(random.choice(range(m, number_of_momnet,1)))

        #TODO:ask professor if a flag must include x and z flag:
        flags = []
        # no z flag and there is more flag than needed
        for q in qubits:
            f = Flag()
            x_flag, z_flag = f.create_flag(q, q)
            if random.choice([True,False]):
                flags.append(x_flag)
            else:
                flags.append(z_flag)

        helper1 = 0
        helper2 = 0
        for i ,moment in enumerate(circuit.moments):
            added_original_moment = False
            for n in range(number_of_flag):
                if helper1 < number_of_flag and start_moments[n] == i:

                    for g in flags[helper1][0]:
                        flag_circuit.append(g,strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                    if not added_original_moment:
                        flag_circuit.append(moment)
                    added_original_moment = True
                    helper1 += 1

                if helper2 < number_of_flag and end_moments[n] == i:
                    print("End")
                    if not added_original_moment:
                        flag_circuit.append(moment)
                    for g in flags[helper2][1]:
                        flag_circuit.append(g,strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
                    added_original_moment = True
                    helper2 += 1
                if helper2 > helper1:
                    print("fail")

            if not added_original_moment :
                flag_circuit.append(moment)
        if  helper1 < number_of_flag or helper2 < number_of_flag:
            print("fail")
        return flag_circuit
    elif stratergy == "heuristic":
        raise NotImplemented



def generate_error_Circuit(circuit: cirq.Circuit, number_of_error: int):
    import  itertools

    def generate_all_error_location():
        re = []
        qubits = list( filter(lambda q:  not 'f' in q.name  ,circuit.all_qubits()))
        moments = list(range( len(circuit.moments)))
        for m in moments:
            for q in qubits:
                re.append([q, m])
        return re
    def generate_error():
        errors = []
        generate_error_helper('', number_of_error, errors)
        print(errors)
        return errors
    def generate_error_helper(current_string, n, strings):
        if len(current_string) == n:
            strings.append(current_string)
        else:
            generate_error_helper(current_string + 'x', n, strings)
            generate_error_helper(current_string + 'z', n, strings)
    def create_error_moments(errors_string,location):
        def helper(error_char,qubit):
            if error_char == 'x':
                return cirq.Moment(cirq.X(qubit))
            elif error_char == 'z':
                return cirq.Moment(cirq.Z(qubit))
        return list(map(lambda a, b: helper(a, b[0]), errors_string, location))

    def add_error_moments(cir: cirq.Circuit, error_moments, location):
        # the varible location should be in the form (qubits,index)
        new_circuit = cirq.Circuit()
        for index , m in enumerate(cir.moments):
            for i, l in enumerate(location):
                if l[1] == index:
                   new_circuit.append(error_moments[i])
            new_circuit.append(m,strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        return new_circuit

    all_error_locations= generate_all_error_location()

    errors_string = generate_error()
    all_combination_of_error_location  = list(itertools.combinations_with_replacement(all_error_locations,number_of_error))
    all_error_circuit= []
    for e in errors_string:
        helper =map( lambda a : [create_error_moments(a[0],a[1]),a[1]]
            ,list(map( lambda l : [e,l] ,all_combination_of_error_location)))
        for i in helper:
            all_error_circuit.append(add_error_moments(circuit, i[0], i[1]))


    return all_error_circuit




def is_moment_with_cnot(momnet: cirq.Moment):
    for op in momnet.operations:
        if len(op.qubits) == 2:
            return True
    return False
