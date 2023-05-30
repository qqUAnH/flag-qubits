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


def generate_error_input(circuit,number_of_error:int):