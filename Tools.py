def cleanString(string):
    """Fonction pour supprimer tous les espaces d'une chaine de caracteres"""
    res = ""
    for char in string:
        if char != ' ':
            res += char
    return res

def replaceSigns(string):
    """Fonction qui inverse les signes plus et moins dans une string"""
    res = ""
    for char in string:
        if char == '+':
            res += '-'
        elif char == '-':
            res += "+"
        else:
            res += char
    return res

def posPuissance(nb, puissance):
    """Fonction qui renvoie un nombre 'nb' a la puissance 'puissance' pour les puissances positives et entieres"""
    if nb >= 0 :
        res = 1
        for i in range(puissance):
            res *= nb
        return res


def sqrt(nb):
    """Fonction qui renvoie la racine carree d'un nombre"""
    if nb == 0.0:
        return 0
    last = nb/2.0
    while True:
        current = (last + nb / last)/2
        valAbs = (current-last) if (current-last) > 0 else (current-last) * (-1)
        if valAbs < 0.00000001:
            return current
        last = current
