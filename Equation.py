import re
from Tools import sqrt, cleanString, replaceSigns, posPuissance
#recoder max aussi au cas ou


class Equation():

    def __init__(self, string):
        """Constructeur de la classe equation"""
        self.eq = string.strip()+ ' '
        self.ok = False if 'deg' in string else True

        self.__left = self.__getLeft()
        self.__right = self.__getRight()

        self.reduced = self.__putEverythingLeft()

        self.__rest = self.reduced

        self.b = []
        self.a = []
        self.c = []
        self.__nb = {} #contient tous les coefficients

        self.__getCoeffs()
        self.__getFinalCoeffs()

        self.__getReduced()
        self.__checkOk()

        self.degree = -1
        self.__checkDegree()


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


    def __putEverythingLeft(self):
        return self.__left.strip() + " " + replaceSigns(self.__right) + " = 0"


    def __getCoeffs(self):
        """Methode permettant de recuperer les coefficients d'un degre donne"""
        Xpattern = r"[+-]\ [0-9]+\.*[0-9]*\ \*\ X\^[0-9]+\ "
        nb = {}
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            degPattern = r"\^[0-9]+\ $"
            deg = re.search(degPattern, value).group(0)[1:-1]
            if deg not in list(nb.keys()):
                nb.update( {deg : [value[:-1]]} )
            else:
                nb[deg] += [value]
            self.__rest = self.__rest.replace(value[:-1], "deg"+deg)

        Xpattern = r"[-+]\ X\^[0-9]+\ "
        for expr in re.finditer(Xpattern,self.__rest):
            value = expr.group(0)
            degPattern = r"\^[0-9]+\ )$"
            deg = re.search(degPattern, value).group(0)[1:-1]
            if deg not in list(nb.keys()):
                nb.update( {deg : [value[:-1]]} )
            else:
                nb[deg] += [value]
            nb += [value[0]+" 1 * X^"+deg]
            self.__rest = self.__rest.replace(value[:-1], 'deg'+deg)

        if "0" in list(nb.keys()):
            self.c = nb["0"]
        if "1" in list(nb.keys()):
            self.b = nb["1"]
        if "2" in list(nb.keys()):
            self.a = nb["2"]
        self.__nb = nb


    def __getFinalCoeffs(self):
        """Methode pour recuperer les coeff ecrit de maniere naturelle"""
        Xpattern = r"[+-]\ [0-9]+\.*[0-9]*\ \*\ X"+' '
        for expr in re.finditer(Xpattern,self.__rest):
            self.__nb["1"] += [expr.group(0)[:-1]+"^1"]
            self.__rest = re.sub(Xpattern[:-1], 'deg1', self.__rest)

        Xpattern = r"[-+]\ X"+" "
        for expr in re.finditer(Xpattern,self.__rest):
            self.__nb["1s"] += [expr.group(0)[0]+" 1 * X^1"]
            self.__rest = re.sub(Xpattern[:-1], 'deg1', self.__rest)

        Xpattern = r"[+-]\ [0-9]+\.*[0-9]*"+" "
        for expr in re.finditer(Xpattern,self.__rest):
            self.__nb["0"] += [expr.group(0)+"* X^0"]
            self.__rest = re.sub(Xpattern[:-1], 'deg0', self.__rest)


    def __getReduced(self):
        """Methode de reduction de  equation"""
        if len(list(self.__nb.keys())) == 0 :
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
            self.ok = False


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
            self.degree = max(list(self.__nb.keys()))


    def getDegree(self):
        """Methode qui renvoie le degre de l'equation"""
        if self.degree > 2:
            print("Polynomial degree:", self.degree)
            print("The polynomial degree is stricly greater than 2, I can't solve.")
            return False
        else:
            print("Polynomial degree:", self.degree)
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
            coeff = cleanString(coeff)
            coeff = re.sub(pattern, '', coeff)
            coeffNb += [float(coeff[1:])]
            coeffSign += [coeff[0]]
        for i in range(len(coeffNb)):
            if coeffSign[i] == '-':
                res -= coeffNb[i]
            else:
                res += coeffNb[i]
        if res.is_integer() == True:
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
        X = (self.c / self.__b) * (-1)
        print("The solution is:")
        print(X)
        return


    def __solve2(self):
        """Methode pour resoudre le polynome de degre 2"""
        delta = posPuissance((self.b),2) - 4*(self.a *self.c)
        if delta < 0:
            print("Determinant is stricly negative. The two complex solutions are:")
            b = str(self.b * (-1))
            twoA = str(self.a * 2)
            complexe = str(sqrt(delta * (-1)))
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
            print(X1)
            print(X2)
        else:
            X = ((self.b)*(-1)) / (2*self.a)
            print ("The solution is:")
            print(X)
        return


    def solve(self):
        """Methode de resolution de l equation"""
        self.a = self.__sumCoeffs(self.a , "2")
        self.b  = self.__sumCoeffs(self.b, "1")
        self.c = self.__sumCoeffs(self.c, "0")
        if self.degree == 0:
            self.__solve0()
        elif self.degree == 1:
            self.__solve1()
        else:
            self.__solve2()
