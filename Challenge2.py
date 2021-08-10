
class BinaryField():
    def __init__(self):
        self.p = '100011011'

    def toBinary(self, n):
        """ Convertit un entier n en un string contenant la séquence binaire de 8 bits."""
        return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])

    def add(self, a, b):
        a = int(a,2)
        b = int(b,2)
        result = bin(a^b)[2:]
        return "0"*(8-len(result))+result

    def multiply(self, a, b):
        b = int(b,2)
        result = "0"
        while b:
            if b & 1:
                result = self.add(a,result)
            a = a + "0"
            b >>= 1
            if int(a,2) & 2**8:
                a = self.add(a,self.p[1:])
        finalResult =str(bin(int(result,2)&(2**(8)-1)))[2:]
        return "0"*(8-len(finalResult))+finalResult

    def inverse(self, a):
        """ Inverse un élément du corps donné sous forme d'une séquence binaire (stockée dans un string).
        La valeur de retour doit aussi être un string.
        Par exemple :
        ('10111001')^(-1) = '10001110'
        """
        b = self.toBinary(1)
        c = a
        for _ in range(8-1):
            c = self.multiply(c, c)
            b = self.multiply(b, c)
        return b


class ReedSolomon():
    def __init__(self, k, n, x):
        self.f = BinaryField()
        self.k = k
        self.n = n
        self.x = x

    def encoding(self, msg_original):
        fonction = self.f
        x = self.x
        a = msg_original
        message = [""]*self.n
        for i in range(0,self.n):
            message[i] = a[-1]
            for j in range(1,len(a)):
                message[i] = fonction.add(fonction.multiply(message[i],x[i]),a[len(a)-1-j])
        return message

    def _lagrangian_interpolation(self, X, Y):
        if len(X) != 4 and len(Y) !=4:
             raise ValueError("Il faut exactement 4 points pour l'interpolation Lagrangienne.")
        x0, x1  = self.f.toBinary(0), self.f.toBinary(1)
        Ytild   = [x1] * self.k
        out     = [x0] * self.k

        for (j, xj, yj) in zip(range(len(X)), X, Y):
            acc = [x1, x0, x0, x1]
            for k, xk in enumerate(X):
                if k != j:
                    Ytild[j] = self.f.multiply(Ytild[j], self.f.add(xj, xk))
                    acc[2]   = self.f.add(acc[2], xk)
                    for xl in [X[l] for l in range(k) if l != j]:
                        acc[1] = self.f.add(acc[1], self.f.multiply(xl, xk))
                    acc[0] = self.f.multiply(acc[0], xk)

            Ytild[j] = self.f.multiply(yj, self.f.inverse(Ytild[j]))
            for i in range(len(out)):
                out[i] = self.f.add(out[i], self.f.multiply(Ytild[j], acc[i]))
        return out

    def decoding(self, msg_corrompu):
        """ Renvoie le message original (uniquement si k=4) qui correspond au message corrompu reçu.
        Dans le message corrompu, au maximum n-4 bytes peuvent être corrompus. Une corruption est le remplacement d'un bit par 'e'.
        Par exemple:
            - Si k=4, n=6;
            - msg_corrompu est de la forme ['11001100', 'e00100e0', '01100000', '10100101', '11e0011e', '11001111']
        """
        if self.k != 4:
             raise ValueError("Le décodage n'est prévu que pour des message de longueur 4.")
        else:
            Y = [""]*4
            X = [""]*4
            index = 0
            get = 0
            for mot in msg_corrompu:
                if "e" not in mot:
                    Y[index] = mot
                    X[index] = self.x[get]
                    index+=1
                get+=1
                if index==4:
                    break
            if len(X)==4:
                a = self._lagrangian_interpolation(X,Y)
                return a
        return None
            
        


solomon = ReedSolomon(4, 6, ['00000000', '00000001', '00000010', '00000011', '00000100', '00000101'])
encode = solomon.encoding(['10011000', '01010111', '00110001', '01000000'])
error = ['10011e00', '10111110', '11000100', 'e1111e01', '01001001', '00011000']
decode = solomon.decoding(error)
print(encode)
print(decode)
"""
ouptut:
['10011000', '10111110', '11000100', '01111001', '01001001', '00011000']
['10011000', '01010111', '00110001', '01000000']
"""

            
    





.