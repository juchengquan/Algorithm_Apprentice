import gurobipy as gb
import numpy as np


class Job_Assignment(object):
    def __init__(self, availablity, shift, if_use_slack=True, num_iteration=100):
        self.wk_aval = availablity
        self.shift = shift

        self.n_worker = self.wk_aval.shape[0]
        self.n_shift = self.wk_aval.shape[1]

        self.model = gb.Model()
        self.model.Params.OutputFlag = 0

        self._if_use_slack = if_use_slack
        self._num_iteration = num_iteration

        self.is_optimal = False
        self.n_removed_cons = 0

    def auto_execution(self):
        self._gen_var()
        self._gen_cons()
        self._set_objective()

        self.optimize()
        self.get_result()

    def _gen_var(self):
        """Generate variables"""
        self.u = [
            [self.model.addVar(vtype="B", name="wk_av[{}][{}]".format(i, j)) for j in range(self.n_shift)]
            for i in range(self.n_worker)
        ]
        self.u_max = self.model.addVar(vtype="I", name="u_max")
        self.u_min = self.model.addVar(vtype="I", name="u_min")

        # 1. first solution is to add slack variables directly:
        if self._if_use_slack:
            self.slack = [self.model.addVar(lb=0, ub=self.n_worker, name="s_{}".format(i)) for i in range(self.n_shift)]

        self.model.update()

    def _gen_cons(self):
        """Generate constraints"""

        # work availability:
        for i in range(self.n_worker):
            for j in range(self.n_shift):
                self.model.addConstr(self.u[i][j] <= self.wk_aval[i][j], name="cons_wk_aval_{0}{1}".format(i,j))

        # get min and max No of working slots
        for i in range(self.n_worker):
            self.model.addConstr(self.u_max >= sum(self.u[i]), name="cons_max_{}".format(i))
            self.model.addConstr(self.u_min <= sum(self.u[i]), name="cons_min_{}".format(i))

        # meet No of shift requirement
        if self._if_use_slack:
            for j in range(self.n_shift):
                self.model.addConstr(sum(self.u[i][j] for i in range(self.n_worker)) >= self.shift[j] - self.slack[j],
                             name="cons_shift_{}".format(j))
        else:
            for j in range(self.n_shift):
                self.model.addConstr(sum(self.u[i][j] for i in range(self.n_worker)) >= self.shift[j],
                              name="cons_shift_{}".format(j))

        self.model.update()

    def _set_objective(self):
        if self._if_use_slack:
            self.model.setObjective(self.u_max - self.u_min + sum(self.slack))
        else:
            self.model.setObjective(self.u_max - self.u_min)

        self.model.update()

    def optimize(self):
        """Execute optimization"""
        self.model.optimize()  # first attampt
        if self.model.status == 2:  # code of optimality Gurobi solver
            self.is_optimal = True

        counter = 1
        while self.model.status != 2 and counter < self._num_iteration:
            removed_list = []
            if self.model.status == 4:  # code of infeasibility 
                self.model.computeIIS()
                cons = self.model.getConstrs()
                for c in cons:
                    if c.IISConstr:
                        removed_list.append(c)
                        self.model.remove(c)

                self.n_removed_cons += len(removed_list)
                if not removed_list:
                    print("The optimization problem is infeasible.")
                    break

                self.model.optimize()
                if self.model.status == 2:
                    self.is_optimal = True


    def get_result(self):
        if not self.is_optimal:
            print("No feasible solution.")
            return

        self.result = self.wk_aval.copy()
        for i in range(self.n_worker):
            for j in range(self.n_shift):
                self.result[i][j] = self.u[i][j].X

        print("The objective value is: {}".format(self.model.ObjVal))
        print("The difference of workload is {}".format(int(self.u_max.X) - int(self.u_min.X)))
        if self._if_use_slack:
            v_slack = sum(self.slack[i].X for i in range(self.n_shift))
            print("The panelty of slackness is {}".format(int(v_slack)))
        else:
            print("The number of removed IIS constraints is {}".format(self.n_removed_cons))

        print("The scheduling is:")
        print(self.result)
        # return self.result


if __name__ == "__main__":
    aval = np.array([
        [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ])

    shifts = np.array(
        [3, 2, 4, 4, 5, 6, 5, 2, 2, 3, 4, 6, 7, 5]
    )

    print("Without slack variables, by removing IIS subproblems: \n")
    h = Job_Assignment(aval, shifts, if_use_slack=False)
    h.auto_execution()

    print("\n\n")
    # Or just use slack variables for infeasible constraints:
    print("Or by adding slack variables: \n")
    h = Job_Assignment(aval, shifts, if_use_slack=True)
    h.auto_execution()








