
import stim

import stim

simulator = stim.TableauSimulator()

# THe ideas is use tableauSImulator and run part of the circuit base on this
simulator.do(stim.Circuit("""
    H 0
    CNOT 0 1
    M 0
"""))

# Do something depending on the measurement result.
latest_measurement_result = simulator.current_measurement_record()[-1]
if latest_measurement_result:
    simulator.do(stim.Circuit("""
        # ...
    """))

# Run the rest of the circuit.
simulator.do(stim.Circuit("""
    
"""))

shot = simulator.current_measurement_record()