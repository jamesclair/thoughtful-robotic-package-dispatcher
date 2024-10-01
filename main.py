STANDARD = "STANDARD"
SPECIAL = "SPECIAL"
REJECTED = "REJECTED"
MIN_BULKY_VOLUME = 1000000
MIN_BULKY_DIMENSION = 150
MIN_HEAVY_MASS = 20


class RoboticArmDispatcher:
    width: float
    height: float
    length: float
    mass: float

    def sort(self, width: float, height: float, length: float, mass: float) -> str:
        # Sort packages with given dimensions and mass into one of 'STANDARD', 'SPECIAL', or 'REJECTED' stacks
        # units are assumed to be cm for the dimensions and kg mass
        self.width = width
        self.height = height
        self.length = length
        self.mass = mass

        self.validate_measurements_gte_zero()

        if self.is_bulky() and self.is_heavy():
            # **REJECTED**: packages that are **both** heavy and bulky are rejected.
            return REJECTED
        elif self.is_bulky() or self.is_heavy():
            # **SPECIAL**: packages that are either heavy or bulky can't be handled automatically.
            return SPECIAL
        # **STANDARD**: standard packages (those that are not bulky or heavy) can be handled normally.
        return STANDARD

    def validate_measurements_gte_zero(self):
        if any(m < 0 for m in [self.width, self.height, self.length, self.mass]):
            raise ValueError(
                f"ERROR: A package measurement was less than or equal to zero check inputs and try again: {self}"
            )

    def get_volume(self):
        return self.width * self.height * self.length

    def has_bulky_dimension(self):
        return max(self.width, self.height, self.length) >= MIN_BULKY_DIMENSION

    def has_bulky_volume(self):
        return self.get_volume() >= MIN_BULKY_VOLUME

    def is_bulky(self):
        return self.has_bulky_dimension() or self.has_bulky_volume()

    def is_heavy(self):
        return self.mass >= MIN_HEAVY_MASS


if __name__ == "__main__":
    arm = RoboticArmDispatcher()

    # test no bulk or heavy mass
    assert (
        arm.sort(
            width=99,
            height=99,
            length=99,
            mass=MIN_HEAVY_MASS - 1,
        )
        >= STANDARD
    )

    # test bulky volume
    assert (
        arm.sort(
            width=100,
            height=100,
            length=100,
            mass=10,
        )
        >= SPECIAL
    )
    # test one bulky dimension
    assert arm.sort(width=MIN_BULKY_DIMENSION, height=99, length=99, mass=10) == SPECIAL
    # test heavy mass
    assert arm.sort(width=99, height=99, length=99, mass=MIN_HEAVY_MASS) == SPECIAL
    # test bulky and heavy
    assert (
        arm.sort(width=MIN_BULKY_DIMENSION, height=100, length=100, mass=MIN_HEAVY_MASS)
        == REJECTED
    )
    # test invalid measurement raises exception
    # NOTE: I'd usually do this with unittest or pytest, but for brevity and remove imports
    is_exception = False
    try:
        arm.sort(width=-1, height=0, length=0, mass=0)
    except ValueError as e:
        is_exception = True

    assert is_exception == True
