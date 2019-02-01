def cleanString(string):
    """Fonction pour supprimer tous les espaces d'une chaine de caracteres"""
    try:
        res = ""
        for char in string:
            if char != ' ':
                res += char
        return res
    except TypeError:
        raise TypeError("First argument must be a string.")


def replaceSigns(string):
    """Fonction qui inverse les signes plus et moins dans une string"""
    try:
        res = ""
        for char in string:
            if char == '+':
                res += '-'
            elif char == '-':
                res += "+"
            else:
                res += char
        return res
    except TypeError:
        raise TypeError("First argument must be a string.")


def posPuissance(nb, puissance):
    """Fonction qui renvoie un nombre 'nb' a la puissance 'puissance' pour les puissances positives et entieres"""
    try:
        res = 1
        for i in range(puissance):
            res *= nb
        return res
    except ValueError:
        raise ValueError("First argument must be a positive number.")


def sqrt(nb):
    """Fonction qui renvoie la racine carree d'un nombre"""
    try:
        if nb == 0.0:
            return 0
        last = nb/2.0
        while True:
            current = (last + nb / last)/2
            valAbs = (current-last) if (current-last) > 0 else (current-last) * (-1)
            if valAbs < 0.00000001:
                return current
            last = current
    except TypeError:
        raise TypeError("The argument must be an int or float number.")


def getMax(liste):
    """Fonction qui renvoie le maximum d'une liste"""
    try:
        res = liste[0]
        for elem in liste:
            if elem > res:
                res = elem
        return res
    except TypeError:
        raise TypeError("The argument must be a list.")


def fraction(nb):
    """Fonction qui transforme un nombre en chaine de caractere et si pertient, en fraction"""
    try:
        if nb == 0:
            return "0"
        if float(nb).is_integer() == True:
            return str(nb)
        for den in range(1,10):
            for num in range(1,den*2):
                if nb == num/den:
                    return str(num)+"/"+str(den)
                if nb == num/den * (-1):
                    return '-'+str(num)+'/'+str(den)
        return str(nb)
    except TypeError:
        raise TypeError("The argument must be a float or integer")

def strToFloat(string):
    """Fonction pour transformer les fractions en float"""
    try:
        if "/" in string:
            slashPos = string.index("/")
            num = float(string[:slashPos])
            den = float(string[slashPos+1:])
            res = num/den
            return res
        else:
            return float(string)
    except TypeError:
        raise TypeError("The argument must be a number loaded in a string")
