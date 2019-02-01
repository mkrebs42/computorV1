import re
from Tools import *

class Equation():


    def __init__(self, string):
        """Constructeur de la classe equation"""
        self.eq = string.strip()+ ' '
        self.ok = self.__checkString()

        self.__left = self.__getLeft()
        self.__right = self.__getRight()

        self.reduced = cleanString(self.__putEverythingLeft())

        self.__rest = self.reduced

        self.b = 0
        self.a = 0
        self.c = 0
        self.__nb = {"0":[], "1":[], "2":[]} #contient tous les coefficients

        self.__getCoeffs()
        self.__getFinalCoeffs()

        self.__getReduced()
        self.__checkOk()

        self.degree = -1
        self.__checkDegree()


    def __checkString(self):
        """Methode pour verifier qu'il n'y a pas de 'deg' dans la string et pas de point suivi d'autre chaoseose qu'un nombre"""
        if 'deg' in self.eq:
            return False

        if '.' in self.eq:
            idx = self.eq.index('.')
            if idx == len(self.eq) - 1:
                return False
            if self.eq[idx+1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return False

        return True


    def __getLeft(self):
        """Methode pour recuperer la partie gauche de l equation"""
        res = self.eq[:self.eq.index('=')].strip()
        if res[0] != '-' and res[0] != '+':
            res = '+ ' + res
        return res


    def __getRight(self):
        """Methode pour recuperer la partie droite de l equation"""
        res = self.eq[self.eq.index('=')+1:].strip()
        if res == "0":
            return ""
        if res[0] != '-' and res[0] != '+':
            res = '+ ' + res
        return res


    def __putEverythingLeft(self):
        return self.__left.strip() + " " + replaceSigns(self.__right) + " = 0"


    def __getCoeffs(self):
        """Methode permettant de recuperer les coefficients d'un degre donne"""
        Xpattern = r"[+-][0-9]+[./]*[0-9]*\*X\^[0-9]+"
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            degPattern = r"\^[0-9]+$"
            nbPattern = r"^[+-][0-9]+[./]*[0-9]*"
            nb = re.search(nbPattern, value).group(0)
            deg = re.search(degPattern, value).group(0)[1:]
            if deg not in list(self.__nb.keys()):
                self.__nb.update( {deg : [nb]} )
            else:
                self.__nb[deg] += [nb]
            self.__rest = self.__rest.replace(value, "deg"+deg)

        Xpattern = r"[-+]X\^[0-9]+"
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            degPattern = r"\^[0-9]+$"
            nb = value[0] + "1"
            deg = re.search(degPattern, value).group(0)[1:]
            if deg not in list(self.__nb.keys()):
                self.__nb.update( {deg : [nb]} )
            else:
                self.__nb[deg] += [nb]
            self.__rest = self.__rest.replace(value, 'deg'+deg)


    def __getFinalCoeffs(self):
        """Methode pour recuperer les coeff ecrit de maniere naturelle"""
        Xpattern = r"[+-][0-9]+[./]*[0-9]*\*X"
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            nbPattern = r"^[+-][0-9]+[./]*[0-9]*"
            nb = re.search(nbPattern, value).group(0)
            self.__nb["1"] += [nb]
            self.__rest = self.__rest.replace(value, 'deg1')

        Xpattern = r"[-+]X"
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            nb = value[0] + " 1"
            self.__nb["1"] += [nb]
            self.__rest = self.__rest.replace(value, 'deg1')

        Xpattern = r"[+-][0-9]+[./]*[0-9]*"
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            nbPattern = r"^[+-]*[0-9]+[./]*[0-9]*"
            nb = re.search(nbPattern, value).group(0)
            self.__nb["0"] += [nb]
            self.__rest = self.__rest.replace(value, 'deg0')


    def __allNullCoeff(self):
        """Methode qui verifie si l equation est de forme "0=0" """
        for key, value in self.__nb.items():
            if self.__sumCoeffs(self.__nb[key], str(key)) != 0 :
                return False
        return True


    def __getReduced(self):
        """Methode de reduction d equation"""
        if self.__allNullCoeff() == True :
            self.reduced = "0 = 0"
            return
        self.reduced = ""
        for deg in list(self.__nb.keys()):
            valueCoeff = self.__sumCoeffs(self.__nb[deg], deg)
            if valueCoeff > 0 :
                if deg == "0":
                    self.reduced += '+ '+ str(valueCoeff) + " "
                elif deg == "1":
                    self.reduced += '+ '+ str(valueCoeff) + " X "
                else :
                    self.reduced += '+ '+ str(valueCoeff) + " * X^" + deg + " "
            elif valueCoeff < 0:
                if deg == "0":
                    self.reduced += '- '+ str(valueCoeff)[1:] + " "
                elif deg == "1":
                    self.reduced += '- '+ str(valueCoeff)[1:] + " X "
                else:
                    self.reduced += '- '+ str(valueCoeff)[1:] + " * X^" + deg + " "
        self.reduced += "= 0"
        self.reduced = self.reduced[2:]


    def __checkOk(self):
        """Methode pour verifier qu'il n'y a pas d'erreur de syntaxe"""
        if self.ok == False:
            return
        self.__rest = cleanString(self.__rest)
        pattern = r"deg[0-9]+"
        for expr in re.finditer(pattern, self.__rest):
            self.__rest = re.sub(pattern, '', self.__rest)
        if self.__rest != "=0":
            raise ValueError("Your equation is not well-typed")


    def __checkDegree(self):
        """Methode pour determiner le degre de l equation"""
        if len(list(self.__nb.keys())) != 0:
            newKeys = []
            newDict = {}
            for key, value in self.__nb.items():
                newKeys += [int(key)]
            newDict = {}.fromkeys(newKeys)
            for key, value in self.__nb.items():
                newDict[int(key)] = value
            self.__nb = newDict

            maximum = 0
            listDeg = list(self.__nb.keys())
            for deg in listDeg:
                if deg > maximum and self.__sumCoeffs(self.__nb[deg], str(deg)) != 0:
                    maximum = deg
            self.degree = maximum


    def getDegree(self):
        """Methode qui renvoie le degre de l'equation"""
        if self.degree > 2:
            print("Polynomial degree:", self.degree)
            print("The polynomial degree is stricly greater than 2, I can't solve.")
            return False
        else:
            print("Polynomial degree:", self.degree)
            return True


    def __sumCoeffs(self, att, deg):
        """Methode qui transforme les attributs degres pour leur donner un seul coefficient"""
        res = 0
        i = 0
        coeffNb = []
        coeffSign = []
        pattern = r"\*X\^"+deg
        for coeff in att:
            coeff = cleanString(coeff)
            coeff = re.sub(pattern, '', coeff)
            coeffNb += [strToFloat(coeff)]
            coeffSign += [coeff[0]]
        for i in range(len(coeffNb)):
            res += coeffNb[i]
        if float(res).is_integer() == True:
            return int(res)
        return res


    def __solve0(self):
        """Methode pour resoudre le polynome de degre 0"""
        if self.c != 0 :
            print("This equation has no solution.")
        else:
            print("All real numbers are solution of this equation")
        return


    def __solve1(self):
        """Methode pour resoudre le polynome de degre 1"""
        X = (self.c / self.b) * (-1)
        print("The solution is:")
        print(fraction(X))
        return


    def __solve2(self):
        """Methode pour resoudre le polynome de degre 2"""
        delta = posPuissance((self.b),2) - 4*(self.a *self.c)
        print(delta)
        if delta < 0:
            print("Determinant is stricly negative. The two complex solutions are:")
            b = fraction(self.b * (-1))
            twoA = fraction(self.a * 2)
            complexe = fraction(sqrt(delta * (-1)))
            if (b == 0):
                z1 = "(i*"+complexe+")/"+twoA
                z2 = "(-i*"+complexe+")/"+twoA
            else:
                z1 = "("+b+"+i*"+complexe+")/"+twoA
                z2 = "("+b+"-i*"+complexe+")/"+twoA
            print(z1)
            print(z2)
        elif delta > 0:
            print("Determinant is stricly positive, the two solutions are:")
            X1 = (self.b*(-1) - sqrt(delta))/(2*self.a)
            X2 = (self.b*(-1) + sqrt(delta))/(2*self.a)
            print(fraction(X1))
            print(fraction(X2))
        else:
            X = ((self.b)*(-1)) / (2*self.a)
            print ("The solution is:")
            print(fraction(X))
        return


    def solve(self):
        """Methode de resolution de l equation"""
        self.a = self.__sumCoeffs(self.__nb[2] ,"2")
        self.b = self.__sumCoeffs(self.__nb[1], "1")
        self.c = self.__sumCoeffs(self.__nb[0], "0")
        print('Considering the equation is formated as "a * X^2 + b * X + c = 0",\na =', self.a, ", b =", self.b, "and c =", self.c)
        if self.degree == 0:
            self.__solve0()
        elif self.degree == 1:
            self.__solve1()
        else:
            print("Polynomial degree is 2, so we calculate the delta : ",end='')
            self.__solve2()
