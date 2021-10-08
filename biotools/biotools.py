# Elimina cualquier caracter que no sea nucleotido
def limpiarCadena(cadena):
    cadenaLimpia = ""
    nucleotidos = ['a', 'c', 'g', 't', 'u']
    for letra in cadena.lower():
        if letra in nucleotidos:
            cadenaLimpia = cadenaLimpia + letra
    return cadenaLimpia


# Lee la cadena de nucleotidos de un archivo de texto plano
def readString(file):
    f = open(file, "r")
    cadena = f.read().strip()
    f.close()
    return cadena


# Retorna un segmento de la cadena original
def segmento(inicio, final, cadena):
    return cadena[inicio - 1:final]


# Nos devuelve la cantidad de cada tipo de nucleotido de una cadena
def nucleotidos(cadena):
    a, c, g, t, u = 0, 0, 0, 0, 0
    for n in cadena:
        if n.lower() == 'a':
            a = a + 1
        if n.lower() == 'c':
            c = c + 1
        if n.lower() == 'g':
            g = g + 1
        if n.lower() == 't':
            t = t + 1
        if n.lower() == 'u':
            u = u + 1
    return {"a": a, "c": c, "g": g, "t": t, "u": u}


# Nos devuelve la cadena complementaria, tanto para ARN como para ADN
def complementaria(cadena, tipus="adn"):
    cc = ""
    for n in cadena.lower():
        if n == "a":
            if tipus == "adn":
                cc = cc + "t"
            else:
                cc = cc + "u"
        if n == "c":
            cc = cc + "g"
        if n == "g":
            cc = cc + "c"
        if n == "t":
            cc = cc + "a"
        if n == "u":
            cc = cc + "a"
        if n == " ":
            cc = cc + " "
    return cc


# Nos retorna la cadena inversa
def inversa(cadena):
    return cadena[::-1]


# Nos retorna el numero de bases (longitud)
def numeroPB(cadena):
    return len(cadena)


# Nos retorna la cadena transcrita
def transcripcion(cadena):
    return cadena.lower().replace('t', 'u')


# Nos retorna los aminoacidos de una cadena (traducción)
def traduccion(cadena):
    proteina = ""
    if len(cadena) % 3 == 0:
        while len(cadena) >= 3:
            codon = cadena[0] + cadena[1] + cadena[2]
            cadena = cadena[3:]
            codon = codon.lower()
            if codon == "gac" or codon == "gau":
                proteina = proteina + "D"
            if codon == "gaa" or codon == "gag":
                proteina = proteina + "E"
            if codon == "gca" or codon == "gcc" or codon == "gcg" or codon == "gcu":
                proteina = proteina + "A"
            if codon == "aga" or codon == "agg" or codon == "cga" or codon == "cgc" or codon == "cgg" or codon == "cgu":
                proteina = proteina + "R"
            if codon == "aac" or codon == "aau":
                proteina = proteina + "N"
            if codon == "ucg" or codon == "ugu":
                proteina = proteina + "C"
            if codon == "uuc" or codon == "uuu":
                proteina = proteina + "F"
            if codon == "gca" or codon == "ggc" or codon == "ggg" or codon == "ggu":
                proteina = proteina + "G"
            if codon == "caa" or codon == "cag":
                proteina = proteina + "Q"
            if codon == "cac" or codon == "cau":
                proteina = proteina + "H"
            if codon == "aua" or codon == "auc" or codon == "auu":
                proteina = proteina + "I"
            if codon == "uua" or codon == "uug" or codon == "cua" or codon == "cuc" or codon == "cug" or codon == "cuu":
                proteina = proteina + "L"
            if codon == "aaa" or codon == "aag":
                proteina = proteina + "K"
            if codon == "aug":
                proteina = proteina + "M"
            if codon == "cca" or codon == "ccc" or codon == "ccg" or codon == "ccu":
                proteina = proteina + "P"
            if codon == "agc" or codon == "agu" or codon == "uca" or codon == "ucc" or codon == "ucg" or codon == "ucu":
                proteina = proteina + "S"
            if codon == "uac" or codon == "uau":
                proteina = proteina + "Y"
            if codon == "aca" or codon == "acc" or codon == "acg" or codon == "acu":
                proteina = proteina + "T"
            if codon == "ugg":
                proteina = proteina + "W"
            if codon == "gua" or codon == "guc" or codon == "gug" or codon == "guu":
                proteina = proteina + "V"
            if codon == "uaa" or codon == "uag" or codon == "uga":
                proteina = proteina + "-"
    return proteina
