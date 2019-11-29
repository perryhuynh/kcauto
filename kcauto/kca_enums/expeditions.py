from datetime import timedelta
from kca_enums.enum_base import EnumBase


class ExpeditionEnum(EnumBase):
    E1_1, E1_2, E1_3, E1_4, E1_5, E1_6, E1_7 = 1, 2, 3, 4, 5, 6, 7
    E1_8, E1_A1, E1_A2, E1_A3, E1_A4 = 8, 100, 101, 102, 103
    E2_9, E2_10, E2_11, E2_12, E2_13, E2_14, E2_15 = 9, 10, 11, 12, 13, 14, 15
    E2_16, E2_B1, E2_B2 = 16, 110, 111
    E3_17, E3_18, E3_19, E3_20, E3_21, E3_22 = 17, 18, 19, 20, 21, 22
    E3_23, E3_24 = 23, 24
    E4_25, E4_26, E4_27, E4_28, E4_29, E4_30 = 25, 26, 27, 28, 29, 30
    E4_31, E4_32 = 31, 32
    E5_33, E5_34, E5_35, E5_36, E5_37, E5_38 = 33, 34, 35, 36, 37, 38
    E5_39, E5_40 = 39, 40
    E7_41, E7_42, E7_43, E7_44 = 41, 42, 43, 44
    EE_S1, EE_S2 = 301, 302

    @property
    def world(self):
        return self.name.split('_')[0][1]

    @property
    def expedition(self):
        return self.name.split('_')[1]

    @property
    def duration(self):
        return DURATIONS[self.value]

    @property
    def display_name(self):
        if self.value == 33:
            return '33 - Node Support'
        elif self.value == 34:
            return '34 - Boss Support'
        elif self.value == 301:
            return 'S1 - Event Node Support'
        elif self.value == 302:
            return 'S2 - Event Boss Node Support'
        return self.name.split('_')[1]


DURATIONS = {
    1: timedelta(minutes=14, seconds=30),
    2: timedelta(minutes=29, seconds=30),
    3: timedelta(minutes=19, seconds=30),
    4: timedelta(minutes=49, seconds=30),
    5: timedelta(hours=1, minutes=29, seconds=30),
    6: timedelta(minutes=39, seconds=30),
    7: timedelta(minutes=59, seconds=30),
    8: timedelta(hours=2, minutes=59, seconds=30),
    100: timedelta(minutes=24, seconds=30),
    101: timedelta(minutes=54, seconds=30),
    102: timedelta(hours=2, minutes=14, seconds=30),
    103: timedelta(hours=1, minutes=49, seconds=30),
    9: timedelta(hours=3, minutes=59, seconds=30),
    10: timedelta(hours=1, minutes=29, seconds=30),
    11: timedelta(hours=4, minutes=59, seconds=30),
    12: timedelta(hours=7, minutes=59, seconds=30),
    13: timedelta(hours=3, minutes=59, seconds=30),
    14: timedelta(hours=5, minutes=59, seconds=30),
    15: timedelta(hours=11, minutes=59, seconds=30),
    16: timedelta(hours=14, minutes=59, seconds=30),
    110: timedelta(minutes=34, seconds=30),
    111: timedelta(hours=8, minutes=39, seconds=30),
    17: timedelta(minutes=44, seconds=30),
    18: timedelta(hours=4, minutes=59, seconds=30),
    19: timedelta(hours=5, minutes=59, seconds=30),
    20: timedelta(hours=1, minutes=59, seconds=30),
    21: timedelta(hours=2, minutes=19, seconds=30),
    22: timedelta(hours=2, minutes=59, seconds=30),
    23: timedelta(hours=3, minutes=59, seconds=30),
    24: timedelta(hours=8, minutes=19, seconds=30),
    25: timedelta(hours=39, minutes=59, seconds=30),
    26: timedelta(hours=79, minutes=59, seconds=30),
    27: timedelta(hours=19, minutes=59, seconds=30),
    28: timedelta(hours=24, minutes=59, seconds=30),
    29: timedelta(hours=23, minutes=59, seconds=30),
    30: timedelta(hours=47, minutes=59, seconds=30),
    31: timedelta(hours=1, minutes=59, seconds=30),
    32: timedelta(hours=23, minutes=59, seconds=30),
    33: timedelta(minutes=15, seconds=30),
    34: timedelta(minutes=29, seconds=30),
    35: timedelta(hours=6, minutes=59, seconds=30),
    36: timedelta(hours=8, minutes=59, seconds=30),
    37: timedelta(hours=2, minutes=44, seconds=30),
    38: timedelta(hours=2, minutes=54, seconds=30),
    39: timedelta(hours=29, minutes=59, seconds=30),
    40: timedelta(hours=6, minutes=49, seconds=30),
    41: timedelta(hours=0, minutes=59, seconds=30),
    42: timedelta(hours=7, minutes=59, seconds=30),
    43: timedelta(hours=11, minutes=59, seconds=30),
    444: timedelta(hours=9, minutes=59, seconds=30),
    301: timedelta(minutes=15),
    302: timedelta(minutes=30)
}
