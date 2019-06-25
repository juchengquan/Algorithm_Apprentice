import pyscipopt as sp

mod = sp.Model()

x1 = mod.addVar()
x2 = mod.addVar()
v =  mod.addVar()

mod.addCons( v == 100*(x2-x1**2)**2 + (1-x1)**2 )

mod.setObjective(v)


mod.optimize()