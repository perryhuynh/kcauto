from kca_enums.enum_base import EnumBase


class OCREnums(EnumBase):
    NUMBERS = '--psm 7 --oem 1 -c tessedit_char_whitelist=0123456789'
    TIMER = '--psm 7 --oem 1 -c tessedit_char_whitelist=0123456789:'
    EXPEDITIONS = '--psm 7 --oem 1 -c tessedit_char_whitelist=ABC0123456789'
