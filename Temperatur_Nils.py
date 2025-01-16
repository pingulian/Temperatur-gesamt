import numpy as np
import sympy
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

class panic(Exception):
    def __init__(self, message = "panic", errors = None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

maxabweichungprozent = 30   #maximale Abweichung in Prozent
#fehler_prozent = 1   #synthetischer Fehler

#val1 = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 24.0, 28.0, 32.0])
#val2 = np.array([29.750, 19.125, 14.375, 9.5, 7.125, 5.625, 4.875, 4.250, 3.750, 3.375, 3.0, 2.625, 2.250, 2.0, 1.875, 1.750, 1.5, 1.375, 1.250])

val1 = np.array([23.56, 22.78, 22.16, 21.43, 20.89, 20.38, 20.17, 19.79, 19.47, 19.12, 18.92, 18.62, 18.59, 18.46, 18.12, 17.98, 17.78, 17.43, 17.21, 17.1, 16.87, 16.78, 16.48, 16.26, 16.1, 15.97, 15.76, 15.53, 15.37, 15.33, 15.3, 15.18, 14.95, 14.58, 14.26, 14.05, 13.98, 13.78, 13.57, 13.39, 13.29, 13.08, 12.82, 12.62, 12.46, 12.33, 12.32, 12.26, 12.2, 12.02, 11.92, 11.9, 11.82, 11.71, 11.63, 11.57, 11.41, 11.28, 11.15, 11.02, 10.84, 10.71, 10.54, 10.42, 10.35, 10.24, 10.11, 10.02, 9.94, 9.79, 9.69, 9.6, 9.52, 9.41, 9.31, 9.18, 9.03, 8.92, 8.84, 8.71, 8.5, 8.48, 8.37, 8.27, 8.18, 8.05, 7.93, 7.82, 7.72, 7.61, 7.51, 7.4, 7.29, 7.17, 7.09, 7, 6.89, 6.82, 6.7, 6.51, 6.47, 6.46, 6.36, 6.26, 6.16, 6.05, 5.97, 5.87, 5.81, 5.71, 5.61, 5.5, 5.42, 5.34, 5.24, 5.1, 4.97, 4.86, 4.71, 4.62, 4.59, 4.52, 4.47, 4.39, 4.35, 4.28, 4.21, 4.18, 4.09, 4.04, 3.97, 3.91, 3.83, 3.76, 3.75, 3.61, 3.56, 3.48, 3.4, 3.35, 3.26, 3.26, 3.22, 3.15, 3.09, 3.02, 2.98, 2.94, 2.91, 2.9])               #Werte 1  
val2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150])              #Werte 2

terme = [np.zeros_like(val1)]

#def synth_fehler(arr,fehlerprozent):
    #index = np.random.randint(0,len(arr))
    #arr[index] += arr[index] * (fehlerprozent/100)
    #return arr

def ratio (val1, val2):
    ratio = (val1/val2)     #/-operator für numpy-arrays implementiert deshalb okay
    return ratio

def product (val1, val2):
    prod = val1*val2
    return prod

def maxerror(values):   #maximale Abweichung vom Mittelwert 
    e = max(np.abs((np.average(values)-np.max(values))), np.abs((np.average(values)-np.min(values))))
    return e

def nichtkonstant(arr,maxabweichungprozent):          #array konstant mit toleranz
    if maxerror(arr) > (maxabweichungprozent/100):
        return True

def monoton_fallend(arr, error_margin_percent):     #array monotom fallend mit toleranz
    error_margin = error_margin_percent / 100
    m = []
    for i in range(0, len(arr)-1 ):
        m.append((arr[i + 1] * (1 - error_margin) < arr[i]) or (arr[i + 1] < arr[i]))
        #print(arr[i + 1] * (1 - error_margin), arr[i],(arr[i + 1] * (1 - error_margin) < arr[i]),arr[i + 1],arr[i],(arr[i + 1] < arr[i]))
    return np.all(m)

def monoton_steigend(arr, error_margin_percent):    #array monoton steigend mit toleranz
    error_margin = error_margin_percent / 100
    m = []
    for i in range(0, len(arr)-1 ):
        m.append((arr[i + 1] * (1 + error_margin) > arr[i]) or (arr[i + 1] > arr[i]))
    return np.all(m)

#val2_new = synth_fehler(val2,fehler_prozent)    #Fehler erzeugen
#print(val2_new)
#val2 = val2_new


term = ""
v1 = "a"    #spätere variablennamen
v2 = "b"    #spätere variablennamen
termstrings = []
n = 0

while nichtkonstant(val2,maxabweichungprozent):             #nicht konstant

    if monoton_steigend(val1, maxabweichungprozent):        #val1 monoton steigend
        if monoton_steigend(val2, maxabweichungprozent):    #val2 monoton steigend
            terme[n] = ratio(val1,val2)                     #quotient bilden
            termstrings.append("(" + v1 + "/" + v2+ ")")    #neuen term hinzufügen
        elif monoton_fallend(val2, maxabweichungprozent):   #val2 monoton fallend
            terme[n] = product(val1,val2)                   #produkt bilden
            termstrings.append("(" + v1 + "*" + v2+ ")")    #neuen term hinzufügen
        else:
            raise panic(message = "val2 nicht monoton " + str(val2) + " " + str(n))     #val2 nicht monoton --> panic
    elif monoton_fallend(val1, maxabweichungprozent):
        if monoton_steigend(val2, maxabweichungprozent):
            terme[n] = product(val1,val2)
            termstrings.append("(" + v1 + "*" + v2+ ")")
        elif monoton_fallend(val2, maxabweichungprozent):
            terme[n] = ratio(val1,val2)
            termstrings.append("(" + v1 + "/" + v2+ ")")
        else:
            raise panic(message = "val2 nicht monoton " + str(val2) + " " + str(n))
    else:
        raise panic(message = "val1 nicht monoton" + str(val1) + " " + str(n))
    

    val1 = val2
    val2 = terme[n]
    terme.append(np.zeros_like(val1))
    v1 = v2
    v2 = termstrings[n]
    n+=1

ax.set_xlabel('Zeit t (in s)')
ax.set_ylabel('Temperatur T (in °C)')        
ax.plot(val1,val2, linewidth=2.0)
plt.show()
  
print (termstrings[-1])                 #term ausgeben (nicht vereinfacht)
print("c= " + str(np.average(val2)))    #Konstante c ausgeben
vereinfacht = sympy.sympify(termstrings[-1])          #term vereinfachen
print(vereinfacht)                      #vereinfachten term ausgeben

