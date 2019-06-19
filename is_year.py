import numpy as np
import pandas as pd

def is_year(in_num):
    if type(in_num) != int:
        raise Exception("the input is not integer!")
    

    if in_num %4 == 0:
        if in_num %100 == 0 and in_num % 400 != 0:
            return 0
        else:
            return 1
    else: 
        return 0

print( is_year(2004) )


class ppp:
    def normal_o(self, inp):
        print(inp)
        
    @staticmethod
    def static_o(inp):
        print(inp)
        
    @classmethod
    def class_o(self,inp):
        print(inp)
        

p = ppp()