import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
import huffmancodec as hc

from scipy.io import wavfile


# Ex. 1


def histograma(file, alfa, alt):
    plt.title(file)
    plt.bar(alfa, alt, 0.5)
    plt.xlabel("Alfabeto")
    plt.ylabel("Número de Ocorrências")
    plt.show()


def altura(P, alfa):
    dicti = dict(zip(alfa, [0] * len(alfa)))

    for i in P:
        dicti[i] += 1

    return dicti


def alfabeto(dim, P, file):
    array = []
    extensao = file.split(".")[1]

    if dim != 1:
        return unique(P)

    if extensao == "txt":
        for i in range(26):
            array += chr(97 + i)
        for i in range(26):
            array += chr(65 + i)

        return np.array(array)
    elif extensao == "bmp":
        return np.array(range(256))
    elif extensao == "wav":
        if P.dtype == "float32":
            return np.array(range(-1, 2))
        elif P.dtype == "int32":
            return np.array(range(-2147483648, 2147483649))
        elif P.dtype == "int16":
            return np.array(range(-32768, 32769))
        elif P.dtype == "uint8":
            return np.array(range(256))


# Ex. 2


def entropia(P, alfa, alt=None):
    H = 0
    if alt is None:
        alt = np.array(list(altura(P, alfa).values()))

    for i in range(len(alfa)):
        if alt[i] != 0:
            H += (alt[i] / len(P)) * math.log2(alt[i] / len(P))

    return round(-H, 4)


# Ex. 3


def readFile(file, dim):
    if dim > 2 or dim < 1:
        print("Dimensão inválida.")
        return

    informacao = fonte(file, dim)
    alfa = alfabeto(dim, informacao, file)

    alt = altura(informacao, alfa)
    alturas = np.array(list(alt.values()))

    if dim == 1:
        histograma(file, alfa, alturas)
    print(file + ":")
    print("Entropia -> " + str(entropia(informacao, alfa, alturas) / dim))
    print("Número médio de bits por símbolo -> " + str(bitsPorSimbolo(informacao, alt) / dim))
    print("Variância dos comprimentos dos códigos -> " + str(variancia(informacao)))
    print("")


def lerTexto(file):
    array = []
    with open(file, "r", encoding="UTF-8", errors="ignore") as f:
        for line in f:
            for char in line:
                if 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122:
                    array += char

    return array


# Ex. 4

def bitsPorSimbolo(P, alt):
    bits = 0

    codec = hc.HuffmanCodec.from_data(P)
    symbols, lengths = codec.get_code_len()

    dicti = dict(zip(symbols, lengths))

    for i in dicti.keys():
        bits += alt[i] * dicti[i]

    return round(bits / len(P), 4)


def variancia(P):
    E1 = E2 = 0

    codec = hc.HuffmanCodec.from_data(P)
    symbols, lengths = codec.get_code_len()

    alt = list(altura(P, symbols).values())

    for i in range(len(lengths)):
        E1 += lengths[i]**2 * alt[i] / len(P)
        E2 += lengths[i] * alt[i] / len(P)

    return round(E1 - E2**2, 4)


# Ex. 5


def fonte(file, dim):
    extensao = file.split(".")[1]

    if extensao == "txt":
        P = lerTexto(file)
    elif extensao == "bmp":
        P = mpimg.imread(file)
    elif extensao == "wav":
        P = wavfile.read(file)[1]
    else:
        print("Extensão inválida.")
        exit(0)

    if dim == 1:
        return np.array(P).flatten()

    P = np.array(P).flatten()
    if P.size % 2 != 0:
        P = P[:-1]

    array = []

    for i in range(len(P) // 2):
        if extensao != "txt":
            array.append(chr(P[i * 2]) + chr(P[i * 2 + 1]))
        else:
            array.append(P[i * 2] + P[i * 2 + 1])

    return np.array(array)


# Ex. 6


def infoMutua(query, target, step):
    array = []
    h_x = entropia(query, np.unique(query))

    for i in range(math.ceil((len(target) - len(query) + 1) / step)):
        window = target[i * step: i * step + len(query)]
        h_y = entropia(window, np.unique(window))

        c = np.c_[window, query]
        new_c = []
        for i in c:
            new_c.append(chr(i[0]) + chr(i[1]))

        h_c = entropia(new_c, unique(new_c))

        array.append(round(h_x + h_y - h_c, 4))

    return array


def unique(P):
    array = []
    for i in P:
        if i not in array:
            array.append(i)

    return array


def Ex6a():
    query = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]
    target = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5, 4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]
    step = 1

    print("Ex 6a:")
    print("Informação Mútua -> " + str(infoMutua(query, target, step)))
    print("")


def Ex6b():
    query = wavfile.read("data/saxriff.wav")[1][:, 0]
    target = wavfile.read("data/target01 - repeat.wav")[1][:, 0]
    step = len(query) // 4

    print("Ex 6b:")
    info = infoMutua(query, target, step)
    print("Informação Mútua (target01 - repeat.wav) -> " + str(info))

    plt.plot(info)

    target = wavfile.read("data/target02 - repeatNoise.wav")[1][:, 0]
    info = infoMutua(query, target, step)
    print("Informação Mútua (target02 - repeatNoise.wav) -> " + str(info))
    print("")

    plt.plot(info)
    plt.show()


def Ex6c():
    query = wavfile.read("data/saxriff.wav")[1][:, 0]
    step = len(query) // 4

    print("Informação Mútua Máxima:")
    for i in range(1, 8):
        file = "data/Song0" + str(i) + ".wav"
        target = wavfile.read(file)[1]
        if target.ndim != 1:
            target = target[:, 0]
        info = infoMutua(query, target, step)
        print(file + " -> " + str(max(info)))
        plt.title(file)
        plt.plot(info)
        plt.show()


readFile("data/lena.bmp", 2)
readFile("data/ct1.bmp", 2)
readFile("data/binaria.bmp", 2)
readFile("data/texto.txt", 2)
readFile("data/saxriff.wav", 2)
Ex6a()
Ex6b()
Ex6c()