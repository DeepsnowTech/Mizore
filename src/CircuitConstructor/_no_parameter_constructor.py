from ._circuit_constructor import CircuitConstructor
from ._greedy_constructor import GreedyConstructor
from Objective._objective import Objective
from PoolGenerator import BlockPool
import time
import numpy
import math
from ParallelTaskRunner._evaluation_task import EvaluationTask
from ParallelTaskRunner import TaskManager
from Blocks import Block, BlockCircuit
from PoolGenerator import BlockPool
from ._result_display import save_construction
from Utilities.Iterators import iter_qsubset
NOT_DEFINED = 999999


class NoParameterConstructor(GreedyConstructor):

    CONSTRUCTOR_NAME = "NoParameterConstructor"

    def __init__(self, construct_obj: Objective, block_pool: BlockPool, n_block_per_iter=1,max_n_iter=100,
                 terminate_cost=0, task_manager: TaskManager = None, init_circuit=None,
                 project_name="Untitled",not_save=False):

        GreedyConstructor.__init__(self, construct_obj, block_pool, max_n_iter=max_n_iter, terminate_cost=terminate_cost,optimizer=None,
                                   no_global_optimization=True, task_manager=task_manager, init_circuit=init_circuit, project_name=project_name,not_save=not_save)
        self.terminate_cost=terminate_cost
        if n_block_per_iter>0:
            self.n_block_per_iter=n_block_per_iter
        else:
            self.n_block_per_iter=len(block_pool.blocks)+n_block_per_iter
        return
    def do_trial_on_circuits_by_cost_value(self, trial_circuits=None):
        assert False
    def do_global_optimization(self):
        assert False
    def do_trial_on_circuits_by_cost_gradient(self, trial_circuits=None):
        if trial_circuits == None:
            trial_circuits = self.trial_circuits
        task_series_id = "SingleBlockEval" + str(self.id % 100000)
        trial_result_list = []
        for trial_circuit in trial_circuits:
            task = EvaluationTask(trial_circuit, None)
            self.task_manager.add_task_to_buffer(task, task_series_id=task_series_id)
        self.task_manager.flush(public_resource={"cost": self.cost})
        res_list = self.task_manager.receive_task_result(
            task_series_id=task_series_id, progress_bar=True)
        for i in range(len(trial_circuits)):
            cost = res_list[i]
            cost_descent = self.current_cost - cost
            # See whether the new entangler decreases the cost
            if cost_descent > 1e-5:
                trial_result_list.append((cost, trial_circuits[i]))
        return trial_result_list

    def update_trial_circuits(self, block_pool=None):
        if block_pool == None:
            block_pool = self.block_pool
        block_pool=list(block_pool)
        self.trial_circuits = []
        pool_size=len(block_pool)
        for subset in iter_qsubset(self.n_block_per_iter,list(range(pool_size))):
            trial_circuit = self.circuit.duplicate()
            for index in subset:
                trial_circuit.add_block(block_pool[index])
            trial_circuit.set_all_block_active()
            self.trial_circuits.append(trial_circuit)