from CircuitConstructor import FixedDepthSweepConstructor, GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import make_example_H2
from HamiltonianGenerator.SpinChainHamiltonian import transverse_field_ising, heisenberg_model
from Blocks import BlockCircuit, HartreeFockInitBlock
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev, \
    jordan_wigner
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool, quasi_imaginary_evolution_rotation_pool, all_rotation_pool
from ParallelTaskRunner import TaskManager

from gauge import get_coverage, get_parameter_efficiency, get_gate_efficiency, get_gate_efficiency_one, get_gate_efficiency_two, \
    get_parameter_efficiency_one, get_parameter_efficiency_two

mole_name="H2"
basis="sto-3g"
transform = jordan_wigner

# Specify energy object(problem)
energy_obj = make_example_H2(basis=basis,fermi_qubit_transform=transform,is_computed=False)
#energy_obj=heisenberg_model(4)

# Generate the block pool
pool=BlockPool(all_rotation_pool(energy_obj.n_qubit,only_odd_Y_operators=True))
#pool = BlockPool(quasi_imaginary_evolution_rotation_pool(energy_obj.hamiltonian))

# Construct the circuit
constructor=GreedyConstructor(
    energy_obj, pool, project_name="_".join([mole_name,basis]), task_manager=TaskManager(n_processor=4))

# Run the constructor
#bc = constructor.execute_construction()
bc = constructor.run()
bc.remove_block(0) # Used to remove initial Hartree block generated by constructor

state_init = '0000'
state_j = '1100'
#print(get_coverage(bc, state_init, state_j))
pe = get_parameter_efficiency(bc, state_init)
ge = get_gate_efficiency(bc, state_init)
peo = get_parameter_efficiency_one(bc, state_init)
geo = get_gate_efficiency_one(bc, state_init)
pet = get_parameter_efficiency_two(bc, state_init)
get = get_gate_efficiency_two(bc, state_init)

# Print out the results to txt file
with open('result.txt', 'a', newline='') as f:
    print("\n{}\n{}\nparameter_efficiency: {}\ngate_efficiency: {}\nparameter_efficiency_one: {}\ngate_efficiency_one: {}\nparameter_efficiency_two: {}\ngate_efficiency_two: {}\n".format(
        'make_example_H2', bc, pe, ge, peo, geo, pet, get), file=f)