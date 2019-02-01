import sys
from Equation import Equation

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise ValueError("You have to enter one parameter.")

    equation = sys.argv[1]

    if "=" not in equation:
        raise ValueError("The sentence you entered is not an equation.")

    eq = Equation(equation)
    if (eq.ok == False):
        raise ValueError("Your sentence is not well-typed.")

    print("Reduced form:", eq.reduced)
    if eq.getDegree() == True:
        eq.solve()
