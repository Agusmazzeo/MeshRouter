import enum
import serial

class SerialParity(enum.Enum):
    NONE = serial.PARITY_NONE
    EVEN = serial.PARITY_EVEN
    ODD = serial.PARITY_ODD
    MARK = serial.PARITY_MARK
    SPACE = serial.PARITY_SPACE

class SerialStopBits(enum.Enum):
    ONE = serial.STOPBITS_ONE
    ONE_POINT_FIVE = serial.STOPBITS_ONE_POINT_FIVE
    TWO = serial.STOPBITS_TWO

class SerialBitSize(enum.Enum):
    FIVE = serial.FIVEBITS
    SIX = serial.SIXBITS
    SEVEN = serial.SEVENBITS
    EIGHT = serial.EIGHTBITS

