import math

class Rational:
   
    _numerator = None
    _denominator = None

    def __init__(self, numerator, denominator):
        self._numerator = numerator
        self._denominator = denominator
    
    def reduce(self):
        gcd = math.gcd(self._numerator, self._denominator)
        self._numerator = self._numerator // gcd
        self._denominator = self._denominator // gcd
    
    def add(self, other):
        return self + other
        
    def __add__(self, other):
        new_denominator = self._denominator * other._denominator
        new_numerator = self._numerator * other._denominator + other._numerator * self._denominator
        return Rational(new_numerator, new_denominator)
    
    def __str__(self):
        return f"{self._numerator} / {self._denominator}"
    
def main():
    a = Rational(24, 36)
    print(a)
    a.reduce()
    print(a)
    b = Rational(2, 3)
    c = a.add(b)
    c.reduce()
    print(c)

main()
