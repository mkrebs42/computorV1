import sys
from Equation import Equation

if __name__ == "__main__":
    equation = sys.argv[1]
    if "=" not in equation:
        print("The sentence you entered is not an equation.")
    else :
        eq = Equation(equation)
        if (eq.ok == False):
            print("Your sentence is not well-typed.")
        else:
            print("Reduced form:", eq.reduced)
            if eq.getDegree() == True:
                eq.solve()
