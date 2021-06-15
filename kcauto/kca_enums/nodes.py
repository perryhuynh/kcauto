from kca_enums.enum_base import EnumBase


class NodeEnum(EnumBase):
    N1, N2, N3, N4, N5, N6, N7, N8, N9, N10 = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    NA, NB, NC, ND, NE, NF, NG, NH = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'
    NI, NJ, NK, NL, NM, NN, NO, NP = 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
    NQ, NR, NS, NT, NU, NV, NW, NX = 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X'
    NY, NZ = 'Y', 'Z'
    NO1, NO2, NO3, NP1, NP2, NP3 = 'O1', 'O2', 'O3', 'P1', 'P2', 'P3'
    NQ1, NQ2, NQ3 = 'Q1', 'Q2', 'Q3'
    NU1, NU2, NU3 = 'U1', 'U2', 'U3'
    NV1, NV2, NV3, NV4, NV5, NV6 = 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'
    NW1, NW2, NW3, NW4, NW5, NW6 = 'W1', 'W2', 'W3', 'W4', 'W5', 'W6'
    NX1, NX2, NX3, NX4, NX5, NX6 = 'X1', 'X2', 'X3', 'X4', 'X5', 'X6'
    NY1, NY2, NY3, NY4, NY5, NY6 = 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6'
    NZ1, NZ2, NZ3, NZ4, NZ5, NZ6 = 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6'
    NZI, NZII = 'ZI', 'ZII'
    NZ7, NZ8, NZ9, NZZ, NZZ1, NZZ2 = 'Z7', 'Z8', 'Z9', 'ZZ', 'ZZ1', 'ZZ2'
    NZZ3 = 'ZZ3'

    @property
    def display_name(self):
        return str(self.value)


class NodeCountEnum(EnumBase):
    N1, N2, N3, N4, N5, N6, N7, N8, N9, N10 = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

    @property
    def display_name(self):
        return str(self.value)


class NamedNodeEnum(EnumBase):
    NA, NB, NC, ND, NE, NF, NG, NH = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'
    NI, NJ, NK, NL, NM, NN, NO, NP = 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
    NQ, NR, NS, NT, NU, NV, NW, NX = 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X'
    NY, NZ = 'Y', 'Z'
    NO1, NO2, NO3, NP1, NP2, NP3 = 'O1', 'O2', 'O3', 'P1', 'P2', 'P3'
    NQ1, NQ2, NQ3 = 'Q1', 'Q2', 'Q3'
    NU1, NU2, NU3 = 'U1', 'U2', 'U3'
    NV1, NV2, NV3, NV4, NV5, NV6 = 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'
    NW1, NW2, NW3, NW4, NW5, NW6 = 'W1', 'W2', 'W3', 'W4', 'W5', 'W6'
    NX1, NX2, NX3, NX4, NX5, NX6 = 'X1', 'X2', 'X3', 'X4', 'X5', 'X6'
    NY1, NY2, NY3, NY4, NY5, NY6 = 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6'
    NZ1, NZ2, NZ3, NZ4, NZ5, NZ6 = 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6'
    NZI, NZII = 'ZI', 'ZII'
    NZ7, NZ8, NZ9, NZZ, NZZ1, NZZ2 = 'Z7', 'Z8', 'Z9', 'ZZ', 'ZZ1', 'ZZ2'
    NZZ3 = 'ZZ3'
