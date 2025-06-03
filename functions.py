#remember, type 1 is degrees and type 0 is radians
import re
import sys

##################################################### Functionality ##############################################
ans = 0
angle_type = 1
help_tutorial =(
"""
Functions:

Basic:

power(base, exponent)
sqrt(base)
absolute(number)

Logarithmic and Exponential:

exp(x) #e^x
ln(x)
log(base, value)

Trignometry:

sin(angle)  csc(angle)  arcsin(angle)
cos(angle)  sec(angle)  arcos(angle)
tan(angle)  cot(angle)  arcot(angle)

Calculus:

derivative( f(x) , point )
integral( lower_limit, upper_limit, f(x) )
solve( f(x) = g(x) , initial_guess )        #equation solver

"""
)

##################################################### LOOKUP TABLE ##############################################
PI = 3.14159265359
E = 2.7182818284590492
DEGREE_TO_RAD = 0.01745329252
RAD_TO_DEGREE = 57.29577951
dx = 0.0001
FN = [
1,
0.5,
0.16666666666666666,
0.041666666666666664,
0.008333333333333333,
0.001388888888888889,
0.0001984126984126984,
2.48015873015873e-05,
2.7557319223985893e-06,
2.755731922398589e-07,
2.505210838544172e-08,
2.08767569878681e-09,
1.6059043836821613e-10,
1.1470745597729725e-11,
7.647163731819816e-13,
4.779477332387385e-14,
2.8114572543455206e-15,
1.5619206968586225e-16,
8.22063524662433e-18,
4.110317623312165e-19,
1.9572941063391263e-20,
8.896791392450574e-22,
3.868170170630684e-23,
1.6117375710961184e-24]

##################################################### HELPERS ##############################################

def spow(base, exponent):
    initial = base
    for _ in range(exponent - 1):
        base *= initial
    return base

def normalize(angle, type):
    if type == 1:
        angle = angle * DEGREE_TO_RAD
    return ((angle + PI) % (2 * PI)) - PI

##################################################### BASIC ##############################################

def absolute(n):
    if n == 0:
        return 0
    elif n < 0:
        return n * -1
    else:
        return n
    
def power(base, exponent):
    if exponent == int(exponent):
        return spow(base, int(exponent))
    elif base < 0:
        if exponent % 2 == 0:
            return power(-base, exponent)
        else:
            return -power(-base, exponent)
    else:
        return exp(exponent * ln(base))

def sqrt(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n < 0:
        raise ValueError("sqrt: negative input")

    x = n/2 if n > 1 else 1
    for _ in range(25):
        factor = (x*x - n)/(2*x)
        x -= factor
    return x


########################################### LOGARITHMIC AND EXPONENTIAL  ################################
#e^x
def exp(x):
    if x == 0:
        return 1
    elif x == 1:
        return E
    elif x < 0 :
        return 1/exp(-x)
    elif int(x) == x:
        return spow(E, int(x))
    elif x < 1:
        t = int(x)
        k = x - t
        numerator = 1.0
        summ = 1.0
        for n in range(1, 24):
            numerator *= k
            summ += numerator*FN[n-1]
        return summ
    else:
        t = int(x)
        k = x - t
        numerator = 1.0
        summ = 1.0

        for n in range(1, 24):
            numerator *= k
            summ += numerator*FN[n-1]
        return summ * spow(E, t)



def ln(n):
    if n == 0:
        return float("-inf")
    elif n == 1:
        return 0    
    elif n < 0:
        raise ValueError("ln: negative input")
    elif n < 1:
        return -ln(1 / n)



    x = 5 if n > 20 else 2.5
    for _ in range(30):
        expx = exp(x)
        factor = (expx - n) / expx
        if abs(factor) < 1e-12: break
        x -= factor
    return x

def log(base, value):
    return ln(value)/ln(base)


##################################################### TRIG ##############################################

def sin(x):
    if angle_type == 1 and x in (0, 30, 45, 60, 90):
        lookup = {0: 0, 30: 0.5, 45: 0.70710678118, 60: 0.86602540378, 90: 1}
        return lookup[x]
    x = normalize(x, angle_type)

    return x - FN[2] * spow(x,3) + FN[4] * spow(x,5) - FN[6] * spow(x,7) + FN[8] * spow(x,9) - FN[10] * spow(x, 11) + FN[12] *spow(x,13) - FN[14] * spow(x, 15) + FN[16] *spow(x,17) - FN[18] *spow(x, 19) + FN[20] *spow(x,21) - FN[22] *spow(x, 23) 

def cos(x):
    if angle_type == 1 and x in (0, 30, 45, 60, 90):
        lookup = {0: 1, 30: 0.86602540378, 45: 0.70710678118, 60: 0.5, 90: 0}
        return lookup[x]
    x = normalize(x, angle_type)
    return 1 - FN[1] * spow(x,2) + FN[3] * spow(x,4) - FN[5] * spow(x,6) + FN[7] * spow(x,8) - FN[9] * spow(x, 10) + FN[11] *spow(x,12) - FN[13] * spow(x, 14) + FN[15] *spow(x,16) - FN[17] * spow(x, 18) + FN[19] *spow(x,20) - FN[21] * spow(x, 22) + FN[23] *spow(x,24)

def tan(x):
    if angle_type == 1 and x in (0, 30, 45, 60, 90):
        lookup = {0: 0, 30: 0.57735026919, 45: 1, 60: 1.73205080757, 90: float('infinite')}
        return lookup[x]
    x = normalize(x, angle_type)
    return sin(x, 0)/cos(x, 0)

def sec(x):
    return 1/sin(x, angle_type)

def csc(x):
    return 1/cos(x, angle_type)

def cot(x):
    return 1/cot(x, angle_type)

def arcsin(n):
    # The Newton - Raphson method for solving equations, where the equation will be sin(x) - n = 0
    x = 0.7071
    for _ in range(25):
        factor = (sin(x, 0) - n) / cos(x, 0)
        x -= factor
        if abs(factor) < 1e-14: break
    if angle_type == 1:
        return x * RAD_TO_DEGREE
    return x

def arcos(n):
    return PI / 2 - arcsin(n, angle_type)

def arctan(n):
    x = 1.62
    for _ in range(25):
        factor = (tan(x, 0) - n) / spow(sec(x, 0), 2) 
        x -= factor
        if abs(factor) < 1e-14: break
    if angle_type == 1:
        return x * RAD_TO_DEGREE
    return x


################################################## CALCULUS ##############################################

def integrate(lower_limit, upper_limtit, equation):
    sum = 0
    x = lower_limit
    while x < upper_limtit:
        sum += dx * eval(equation)
        x += dx
    return sum

def solve(equation, initial_guess):
    #doesn't work well with trig functions
    x = initial_guess
    factor = eval(equation)/derivative(equation, x)
    while absolute(factor) > 1e-10:
        x -= factor
        factor = eval(equation)/derivative(equation, x)
    return x

def derivative(equation, point):
    x = point + dx
    a = eval(equation)
    x = point - dx
    b = eval(equation)
    c = 2*dx

    return (a - b)/c

def convert(s):
    pattern = r'solve\(\s*(.+)\s* = \s*(.+)\s*,'
    replacement = r'solve("\1 + (-1 * \2)",'
    s = re.sub(pattern, replacement, s)
    return s


def main():
    while True:
        user_input = convert(input("input: "))
        if user_input == "deg":
            angle_type = 1
        elif user_input == "rad":
            angle_type = 0
        elif (user_input.lower() == "quit"):
            sys.exit()

        elif user_input.lower() == "help":
            print(help_tutorial)
        else:
            user_input = eval(user_input)
            ans = user_input
            print(round(user_input,  10))

if __name__ == "__main__":
    main()
