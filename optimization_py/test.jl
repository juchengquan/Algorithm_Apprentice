using JuMP
using Gurobi
mod = Model(with_optimizer(Gurobi.Optimizer))
x = @variable(mod, [1:3])