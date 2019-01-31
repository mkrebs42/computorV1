import sys
from Equation import Equation

if __name__ == "__main__":
    equation = sys.argv[1]
    eq = Equation(equation)
    print("Reduced form:", eq.reduced[2:])
    if eq.checkDegree() == True:
        print("Polynomial degree:", eq.degree)
        eq.solve()
