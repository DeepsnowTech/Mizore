from Blocks import BlockCircuit
from Utilities.CircuitEvaluation import evaluate_ansatz_0000_amplitudes
from Blocks._utilities import concatenate_circuit,get_inverse_circuit

def get_inner_product_task_on_sparse_circuit(first_circuit:BlockCircuit,second_circuit:BlockCircuit):
    circuit = concatenate_circuit(
        first_circuit, get_inverse_circuit(second_circuit))
    return get_0000_amplitude_on_sparse_circuit(circuit)

def get_0000_amplitude_on_sparse_circuit(circuit):

    disjoint_sets=circuit.get_disjoint_active_sets()
    localized_circuits=[]
    for qset in disjoint_sets:
        localized_circuits.append(get_localized_circuit(circuit,qset))
    amp_0000=1
    for circuit in localized_circuits:
        circuit.avoid_redundant_qubit()
        pcircuit=circuit.get_ansatz()
        #print(pcircuit.n_qubit)
        amp_0000*=evaluate_ansatz_0000_amplitudes(pcircuit.n_qubit,pcircuit.ansatz)
    return amp_0000

def get_localized_circuit(_circuit:BlockCircuit,qsubset):
    """
    qsubset should be a disjoint set of qubit generated by get_disjoint_active_sets()
    """
    circuit=_circuit.duplicate()
    remove_list=[]
    for i in range(len(circuit.block_list)):
        block=circuit.block_list[i]
        if block.IS_LOCALIZE_AVAILABLE:
            circuit.block_list[i]=block.get_localized_operator(qsubset)
        else:
            if block.qsubset[0] not in qsubset:
                remove_list.append(i)
    for i in reversed(remove_list):
        circuit.block_list.pop(i)
    return circuit
    