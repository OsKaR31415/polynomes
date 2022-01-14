from special_zero import *

def add_iterables(iter1, iter2):
    """Addition of 2 iterables, element by element.
    Works even on endless iterables."""
    v1, v2 = next(iter1), next(iter2)
    if isinstance(v1, SpecialZero) and isinstance(v2, SpecialZero):
        yield from ZeroForever()
    else:
        yield v1 + v2
        yield from add_iterables(iter1, iter2)

def sub_iterables(iter1, iter2):
    """Substraction of 2 iterables, element by element.
    Works even on endless iterables."""
    yield next(iter1) - next(iter2)
    yield from add_iterables(iter1, iter2)

def mult_all(element, iterable):
    i = next(iterable)
    if isinstance(i, SpecialZero):
        yield from ZeroForever()
    else:
        yield i * element
        yield from mult_all(element, iterable)

def inverse(iterable):
    i = next(iterable)
    if isinstance(i, SpecialZero):
        yield from ZeroForever()
    else:
        yield 1 / i
        yield from inverse(iterable)

class Polynom:
    """Class that defines polynoms, and how to combine them.
    These polynoms are made so that teir coefficients could be anything that
    can be added, substracted, multiplied and divided.

    IMPORTANT: the coefficients are reversed compared to the convetionnal order.
    The main reason for that is that the implementation is very next to the
    mathematical definition of polynoms, that is using that order.

    Example:
        >>> one = Polynom([1])
        >>> identity = Polynom([0, 1])  # means 0 + 1*x
        >>> double = Polynom([0, 2])  # means 0 + 2*x
        >>> x_plus_one = Polynom([1, 1])  # means 1 + 1*x
        >>> x_squared = Polynom([0, 0, 1])  # means 0 + 0*x + 1*x**2
        >>> poly = x_squared + one  # adding up two polynoms makes a new one !
        >>> x_squared + x_plus_one  # add up two ones... easy to guess !
    """

    def __init__(self, coeffs: list[int or float]) -> None:
        if isinstance(coeffs, (list, tuple)):
            coeffs = list(coeffs)
            # the loop removes all 0 at the end of coeffs, since they are useless
            while coeffs[-1] == 0:
                coeffs = coeffs[:-1]
            # be carefull that polynom is a function thar returns an iterator !
            self.__polynom = self.__generate_polynom_from_coeffs__(coeffs)
        # if it is a function, we assume that it is a valid generator
        elif type(coeffs) == "<class 'function'>":
            # just "wrap" it with a function
            self.__polynom = lambda _: coeffs

    def __generate_polynom_from_coeffs__(self, coeffs: list[int or float]):
        """In fact, a polynom is a generator, so that is just a wrapper.
        This function returns a function that is the real polynom.
        The returned function is a generator for the coefficients."""
        def polynom():
            """That is the definition of a polynom from its coefficients"""
            for c in coeffs:
                yield c
            yield from ZeroForever()
        return polynom

    def __call__(self, x: int or float) -> int or float:
        result = 0
        power = 0
        polynom = self.__polynom()
        coeff = next(polynom)
        while not isinstance(coeff, SpecialZero):
            # print("coeff :", coeff)
            result += coeff * x**power
            power += 1
            coeff = next(polynom)
        return result

    def get_coeffs(self) -> list[int or float]:
        """Get the coefficients of the current polynom."""
        poly = self.__polynom()
        coeff = next(poly)
        list_coeffs = list()
        while not isinstance(coeff, SpecialZero):
            list_coeffs.append(coeff)
            coeff = next(poly)
        return list_coeffs

    def get_polynom(self):
        return self.__polynom()

    def opposite(self):
        """Return the opposite of a polynom."""
        coeffs = self.get_coeffs()  # get the coefficients
        opposite_coeffs = list(map(lambda x: -x, coeffs))  # negate each one
        return Polynom(opposite_coeffs)  # return the new polynom

    def __add__(self, other):
        if not isinstance(other, Polynom):
            raise TypeError(f"unsupported operand type for +: 'Polynom' and {type(other)}")
        return add_iterables(self.__polynom, other.__polynom)

    def __sub__(self, other):
        if not isinstance(other, Polynom):
            raise TypeError(f"unsupported operand type for -: 'Polynom' and {type(other)}")
        return sub_iterables(self.__polynom, other.__polynom)

    def __mul__(self, other):
        """Return self*other.
        """
        # Polynom * Polynom -> Polynom
        if isinstance(other, Polynom):
            # TODO: implement that one
            raise NotImplementedError
        # else: numbers, or anything that multiplies with the coefficients
        else:
            # get the coefficients of *self*
            coeffs = self.get_coeffs()
            # multiply every coefficient by *other*
            coeffs = list(map(lambda x: x*other, coeffs))
            # return the new polynom
            return Polynom(coeffs)
    def __rmul__(self, other):
        """Return other*self."""
        # hopefully multiplication is commutative
        return self * other

    def __str__(self):
        return '(' + str(self.get_coeffs())[1:-1] + ', Ø...)'
    def __repr__(self):
        return "Polynom(" + str(self.get_coeffs()) + ')'

one      = Polynom([1])
two      = Polynom([2])
identity = Polynom([0, 1])
square   = Polynom([0, 0, 1])
cube     = Polynom([0, 0, 0, 1])

my_polynom = cube + identity + identity + two

print(my_polynom)

for x in range(20):
    print(my_polynom(x), square(x) + 2*identity(x) + two(x))


