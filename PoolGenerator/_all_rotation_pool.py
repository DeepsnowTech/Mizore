from PoolGenerator._block_pool import BlockPool
from Blocks._rotation_entangler import RotationEntangler
from Utilities.Iterators import iter_qsubset_odd_Y_pauli_by_length,iter_all_qsubset_pauli_by_length

class AllRotationPool(BlockPool):
    """Block pool contains all the possible RotationEntangler.
    Attributes:
        only_odd_Y_operators: If true, only RotationEntangler whose Pauli word only has odd number of Y operators will be added.
        Even Y entanglers are exclueded because they commute with Hamiltonian without imaginary terms (usually because of the absense of magnetic field), which means 
        d/dt <psi|e^{-iPt}He^{iPt}|psi> = 0,
        for all the state |psi>
    """
    def __init__(self,n_qubit,max_length=-1,only_odd_Y_operators=True):
        BlockPool.__init__(self)
        self.only_odd_Y_operators=only_odd_Y_operators
        if max_length==-1:
            max_length=n_qubit
        
        if only_odd_Y_operators:
            for qsubset,pauli in iter_qsubset_odd_Y_pauli_by_length(max_length,range(n_qubit)):
                self.blocks.add(RotationEntangler(qsubset,pauli))
        else:
            for qsubset,pauli in iter_all_qsubset_pauli_by_length(max_length,range(n_qubit)):
                self.blocks.add(RotationEntangler(qsubset,pauli))
