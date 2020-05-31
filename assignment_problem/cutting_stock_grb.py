import gurobipy as gb
import numpy as np


class Cutting_Stock(object):
    def __init__(self, length, quantity, b_stock, num_iteration=10):
        self.length = length
        self.quantity = quantity
        self.b_stock = b_stock
        self._num_iteration = num_iteration

        self.master = gb.Model("master")
        self.relax = None
        self.slave = gb.Model("slave")
        self.master.Params.OutputFlag = 0  # surpress the output
        self.slave.Params.OutputFlag = 0  # surpress the output

        self.x = None  # primal problem variable
        self.y = None  # dual problem variable
        self.lam = None  # multiplier of primal constraints
        self.cons = dict()

        self.res_x = None

        self.all_cut_pattern = []

        self.auto_execution()

    def auto_execution(self):
        self._gen_initial_cut_pattern()
        self._initiate_original_prob()
        # self.optimize()

    def _gen_initial_cut_pattern(self):
        self.all_cut_pattern = np.eye(self.num_cons, dtype=int)

    def _initiate_original_prob(self):
        """formulate original problem"""
        self.x = np.array([None] * self.num_vars)
        for i in range(self.num_vars):
            self.x[i] = self.master.addVar(vtype="I", obj=1)
        self.master.update()

        for i in range(self.num_cons):
            self.cons[i] = self.master.addConstr(
                self.x @ self.all_cut_pattern[:, i] >= self.quantity[i]
            )
        self.master.update()

    def optimize(self):
        counter = 1
        while counter < self._num_iteration:
            # Solve the relaxed version:
            self.relax = self.master.relax()
            self.relax.optimize()
            lam_cons = np.array([ele.Pi for ele in self.relax.getConstrs()])

            self.y = np.array([self.slave.addVar(vtype="I", lb=0) for _ in range(self.num_cons)])
            self.slave.update()

            self.slave.addConstr(self.y @ np.array(self.length) <= b_stock)
            self.slave.setObjective(-self.y @ lam_cons)
            self.slave.optimize()

            # get new columns from dual problem
            new_cut_pattern = [int(ele.X) for ele in self.y]

            # add new cuts with early termination
            if new_cut_pattern not in self.all_cut_pattern.tolist():
                self.all_cut_pattern = np.concatenate((self.all_cut_pattern,
                                                       np.array(new_cut_pattern).reshape(1, -1)))
            else:
                print("Early termination as the cutting method has existed: {}.".format(new_cut_pattern))
                print("Terminate at iteration {}. \n".format(counter))
                break

            # add new var to master:
            new_col = gb.Column()
            for i in range(self.num_cons):
                new_col.addTerms(new_cut_pattern[i], self.cons[i])
            self.x = np.append(self.x, None)
            self.x[self.num_vars-1] = self.master.addVar(vtype="I", obj=1, column=new_col)
            self.master.update()

            counter += 1

        # if max no iteration or early termination is reached, optimize original problem
        self.master.optimize()
        self.res_x = np.array([int(self.x[i].X) for i in range(self.num_vars)])

    def get_result(self):
        if self.master.status == 2:
            print("The number of pipes required is {}.".format(int(self.master.ObjVal)))

            print("Length: {}    ".format(self.length))
            print("Quantity: {}".format(self.quantity))
            print("Cut method - Quantity")
            for i, ele in enumerate(self.res_x):
                if ele > 0:
                    print(self.all_cut_pattern[i], " - ", ele)

    @property
    def num_vars(self):
        return len(self.all_cut_pattern)

    @property
    def num_cons(self):
        return len(self.length)


if __name__ == "__main__":
    b_stock = 20
    leng = [3, 7, 9, 16]
    quan = [25, 30, 14, 8]

    h = Cutting_Stock(leng, quan, b_stock)
    h.optimize()
    h.get_result()
