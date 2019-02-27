import sys
from Equation import Equation

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise ValueError("You have to enter one parameter (an equation).")

    equation = sys.argv[1]

    try:
        eq = Equation(equation)
        print("Reduced form:", eq.reduced)
        if eq.getDegree() == True:
            eq.solve()
    except ValueError:
        raise ValueError("Bad parameter format")
