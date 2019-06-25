from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt  

m = GEKKO()
tf = 40
m.time = np.linspace(0,tf,2*tf+1)
step = np.zeros(2*tf+1)
step[3:40] = 2.0
step[40:]  = 5.0

# Controller model
Kc = 15.0                    # controller gain
tauI = 2.0                  # controller reset time
tauD = 1.0                  # derivative constant
OP_0 = m.Const(value=0.0)   # OP bias
OP = m.Var(value=0.0)       # controller output
PV = m.Var(value=0.0)       # process variable
SP = m.Param(value=step)    # set point
Intgl = m.Var(value=0.0)    # integral of the error
err = m.Intermediate(SP-PV) # set point error
m.Equation(Intgl.dt()==err) # integral of the error
m.Equation(OP == OP_0 + Kc*err + (Kc/tauI)*Intgl - PV.dt())

# Process model
Kp = 0.5                    # process gain
tauP = 10.0                 # process time constant
m.Equation(tauP*PV.dt() + PV == Kp*OP)

m.options.IMODE=4
m.solve(disp=False)

plt.figure()
plt.subplot(2,1,1)
plt.plot(m.time,OP.value,'b:',label='OP')
plt.ylabel('Output')
plt.legend()
plt.subplot(2,1,2)
plt.plot(m.time,SP.value,'k-',label='SP')
plt.plot(m.time,PV.value,'r--',label='PV')
plt.xlabel('Time (sec)')
plt.ylabel('Process')
plt.legend()
plt.show()