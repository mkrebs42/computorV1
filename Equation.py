import re
from math import sqrt

#a checker : qu il y a bien un signe =
#que le degre n est pas trop grand
#qu il ny a pas de caractere en trop

class Equation():

    def __cleanString(self, string):
        """Fonction pour supprimer tous les espaces d'une chaine de caracteres"""
        res = ""
        for char in string:
            if char != ' ':
                res += char
        return res

    def __init__(self, string):
        """Constructeur de la classe equation"""
        self.eq = string.strip()

        self.__left = self.__getLeft()
        self.__right = self.__getRight()

        self.reduced = self.__putEverythingLeft()

        self.__rest = self.reduced

        self.__b = self.__getDeg(1)
        self.__a = self.__getDeg(2)
        self.__c = self.__getDeg(0)

        self.__getFinalDeg()

        self.degree = -1


    def __getLeft(self):
        """Methode pour recuperer la partie gauche de l equation"""
        res = self.eq[:self.eq.index('=')].strip()
        if res[0] != '-' and res[0] != '+':
            res = '+ ' + res
        return res


    def __getRight(self):
        """Methode pour recuperer la partie droite de l equation"""
        res = self.eq[self.eq.index('=')+1:].strip()
        if res[0] != '-' and res[0] != '+':
            res = '+ ' + res
        return res


    def replaceSigns(self, string):
        res = ""
        for char in string:
            if char == '+':
                res += '-'
            elif char == '-':
                res += "+"
            else:
                res += char
        return res


    def __putEverythingLeft(self):
        return self.__left.strip() + " " + self.replaceSigns(self.__right) + " = 0"


    def __getDeg(self, deg):
        """Methode permettant de recuperer les coefficients d'un degre donne"""
        Xpattern = r"\+*-*\ ?[0-9]+\ \*\ X\^"+str(deg)+' '
        nb = []
        for expr in re.finditer(Xpattern,self.__rest):
            nb += [expr.group(0)]
            self.__rest = re.sub(Xpattern[:-1], 'deg'+str(deg), self.__rest)
        Xpattern = r"\+*-*X\^"+str(deg)+' '
        for expr in re.finditer(Xpattern,self.__rest):
            print("EXPR GROUP",expr.group(0))
            nb += ["+ 1 * X^"+str(deg)]
            self.__rest = re.sub(Xpattern[:-1], 'deg'+str(deg), self.__rest)
        print(self.__rest)
        return nb

    def __getFinalDeg(self):
        """Methode pour recuperer les coeff ecrit de maniere naturelle"""
        Xpattern = r"[-+]\ [0-9]+\ *"
        for expr in re.finditer(Xpattern,self.__rest):
            print("EXPR GROUP",expr.group(0))
            self.__c += [expr.group(0)+"* X^0"]
            self.__rest = re.sub(Xpattern[:-1], 'deg0', self.__rest)
        Xpattern = r"[-+]\ [0-9]+\ X\ *"
        for expr in re.finditer(Xpattern,self.__rest):
            print("EXPR GROUP",expr.group(0))
            self.__b += [exp.group(0)[:-1]+"^1"]
            self.__rest = re.sub(Xpattern[:-1], 'deg1', self.__rest)
        print("FINAL REST",self.__rest)
        print("deg1", self.__b)
        print("deg0", self.__c)

    def checkDegree(self):
        """Methode pour verifier qu'il s'agit d'une equation de degre 2 ou inf."""
        degPattern = r"X\^[0-9]+"
        deg = []
        for expr in re.finditer(degPattern, self.__rest):
            deg += [int(expr.group(0)[2:])]
            self.__rest = re.sub(degPattern, '', self.__rest)
        if len(deg) > 0:
            maxDeg = max(deg)
            print("Polynomial degree:", maxDeg)
            print("The polynomial degree is stricly greater than", max(deg), ", I can't solve.")
            return False
        if (len(self.__a) > 0):
            self.degree = 2
        elif (len(self.__b) > 0):
            self.degree = 1
        else:
            self.degree = 0
        return True


    def checkClear(self):
        """Methode qui verifie que la string passee en caractere est bien une equation"""
        print("RESTE A LA FIN", self.__rest)
        if len(self.__rest) > 0:
            print("The string is not a go")


    def __sumCoeffs(self, att, deg):
        """Methode qui transforme les attributs degres pour leur donner un seul coefficient"""
        res = 0
        i = 0
        coeffNb = []
        coeffSign = []
        pattern = r"\*X\^"+deg
        for coeff in att:
            coeff = self.__cleanString(coeff)
            coeff = re.sub(pattern, '', coeff)
            coeffNb += [int(coeff[1:])]
            coeffSign += [coeff[0]]
        for i in range(len(coeffNb)):
            if coeffSign[i] == '-':
                res -= coeffNb[i]
            else:
                res += coeffNb[i]
        return res

    def __solve0(self):
        """Methode pour resoudre le polynome de degre 0"""
        if self.__c != 0 :
            print("This equation has no solution.")
        else:
            print("All real numbers are solution of this equation")
        return

    def __solve1(self):
        """Methode pour resoudre le polynome de degre 1"""
        X = (self.__c / self.__b) * (-1)
        print("The solution is:")
        print(X)
        return


    def __solve2(self):
        """Methode pour resoudre le polynome de degre 2"""
        print("B=",self.__b)
        print("A=", self.__a)
        print("C=",self.__c)
        delta = (self.__b)**2 - 4*(self.__a*self.__c)
        print("DELTA=", delta)
        if delta < 0:
            print("The equation has no solution")
        elif delta > 0:
            print("Determinant is stricly positive, the two solutions are:")
            X1 = (self.__b*(-1) - sqrt(delta))/(2*self.__a)
            X2 = (self.__b*(-1) + sqrt(delta))/(2*self.__a)
            print(X1)
            print(X2)
        else:
            X = ((self.__b)*(-1)) / (2*self.__a)
            print ("The solution is:")
            print(X)
        return


    def solve(self):
        """Methode de resolution de l equation"""
        self.__c = self.__sumCoeffs(self.__c, "0")
        self.__b = self.__sumCoeffs(self.__b, "1")
        self.__a = self.__sumCoeffs(self.__a, "2")
        if self.degree == 0:
            self.__solve0()
        elif self.degree == 1:
            self.__solve1()
        else:
            self.__solve2()
