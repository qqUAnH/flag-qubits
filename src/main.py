# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import from_cirq_toICM
import to_FT_flag_circuit
import cirq

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stabcode = ["XZZXI",
                "IXZZX",
                "XIXZZ",
                "ZXIXZ"]
    cir = from_cirq_toICM.single_gate()
    new_cir = from_cirq_toICM.decompose_to_ICM(cir)
    print(to_FT_flag_circuit.encode(cir,   stabcode))
    print("old circuit:\n")
    print(cir)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
