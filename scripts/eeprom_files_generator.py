class MicroCode:
    def __init__(self, micro_code_bits: int, control_line_bits: int) -> None:
        self.micro_code_bits = micro_code_bits
        self.control_line_bits = control_line_bits


EEPROM_SIZE_IN_BYTES = 8192

## Instructions: #########################################################################################
NOP =         0b0000
LDAx =        0b0001
STAx =        0b0010
ADDx =        0b0011
SUBx =        0b0100
JMPx =        0b0101
_RESERVED1_ = 0b0110
_RESERVED2_ = 0b0111
_RESERVED3_ = 0b1000
_RESERVED4_ = 0b1001
_RESERVED5_ = 0b1010
_RESERVED6_ = 0b1011
_RESERVED7_ = 0b1100
_RESERVED8_ = 0b1101
OUT =         0b1110
HLT =         0b1111
##########################################################################################################

## Control bits: #########################################################################################
Cstop =       0b0000000000000001
RCreset =     0b0000000000000010
PCin =        0b0000000000000100
PCout =       0b0000000000001000
PCincrement = 0b0000000000010000
MARin =       0b0000000000100000
RAMin =       0b0000000001000000
RAMout =      0b0000000010000000
IRin =        0b0000000100000000
IRout =       0b0000001000000000
RAin =        0b0000010000000000
RAout =       0b0000100000000000
RBin =        0b0001000000000000
ALUout =      0b0010000000000000
ALUsubtract = 0b0100000000000000
ORin =        0b1000000000000000

INVERTED_LOGIC_MASK = 0b0010101010001101
##########################################################################################################

## Micro-codes: ##########################################################################################
MICRO_CODES = [
    MicroCode(0 | (NOP << 3), PCout | MARin),
    MicroCode(1 | (NOP << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (NOP << 3), RCreset),

    MicroCode(0 | (LDAx << 3), PCout | MARin),
    MicroCode(1 | (LDAx << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (LDAx << 3), IRout | MARin),
    MicroCode(3 | (LDAx << 3), RAMout | RAin),
    MicroCode(4 | (LDAx << 3), RCreset),

    MicroCode(0 | (STAx << 3), PCout | MARin),
    MicroCode(1 | (STAx << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (STAx << 3), IRout | MARin),
    MicroCode(3 | (STAx << 3), RAout | RAMin),
    MicroCode(4 | (STAx << 3), RCreset),

    MicroCode(0 | (ADDx << 3), PCout | MARin),
    MicroCode(1 | (ADDx << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (ADDx << 3), IRout | MARin),
    MicroCode(3 | (ADDx << 3), RAMout | RBin),
    MicroCode(4 | (ADDx << 3), ALUout | RAin),
    MicroCode(5 | (ADDx << 3), RCreset),

    MicroCode(0 | (SUBx << 3), PCout | MARin),
    MicroCode(1 | (SUBx << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (SUBx << 3), IRout | MARin),
    MicroCode(3 | (SUBx << 3), RAMout | RBin),
    MicroCode(4 | (SUBx << 3), ALUsubtract | ALUout | RAin),
    MicroCode(5 | (SUBx << 3), RCreset),

    MicroCode(0 | (JMPx << 3), PCout | MARin),
    MicroCode(1 | (JMPx << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (JMPx << 3), IRout | PCin),
    MicroCode(3 | (JMPx << 3), RCreset),

    MicroCode(0 | (_RESERVED1_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED1_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED1_ << 3), RCreset),

    MicroCode(0 | (_RESERVED2_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED2_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED2_ << 3), RCreset),

    MicroCode(0 | (_RESERVED3_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED3_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED3_ << 3), RCreset),

    MicroCode(0 | (_RESERVED4_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED4_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED4_ << 3), RCreset),

    MicroCode(0 | (_RESERVED5_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED5_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED5_ << 3), RCreset),

    MicroCode(0 | (_RESERVED6_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED6_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED6_ << 3), RCreset),

    MicroCode(0 | (_RESERVED7_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED7_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED7_ << 3), RCreset),

    MicroCode(0 | (_RESERVED8_ << 3), PCout | MARin),
    MicroCode(1 | (_RESERVED8_ << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (_RESERVED8_ << 3), RCreset),

    MicroCode(0 | (OUT << 3), PCout | MARin),
    MicroCode(1 | (OUT << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (OUT << 3), RAout | ORin),
    MicroCode(3 | (OUT << 3), RCreset),

    MicroCode(0 | (HLT << 3), PCout | MARin),
    MicroCode(1 | (HLT << 3), RAMout | IRin | PCincrement),
    MicroCode(2 | (HLT << 3), Cstop)
]
##########################################################################################################


def convert_digit_to_7_segments_bits(digit: int) -> int:
    match digit:
        case 0:
            return 0b00111111
        case 1:
            return 0b00000110
        case 2:
            return 0b01011011
        case 3:
            return 0b01001111
        case 4:
            return 0b01100110
        case 5:
            return 0b01101101
        case 6:
            return 0b01111101
        case 7:
            return 0b00000111
        case 8:
            return 0b01111111
        case 9:
            return 0b01101111
    return 0b00000000

def generate_data_for_instruction_decoder_eeprom(eeprom_index: int) -> bytes:
    data = bytearray(EEPROM_SIZE_IN_BYTES)
    for i in range(len(data)):
        if (eeprom_index == 0):
            data[i] = INVERTED_LOGIC_MASK & 0b11111111
        elif (eeprom_index == 1):
            data[i] = INVERTED_LOGIC_MASK >> 8
    for i in range(len(MICRO_CODES)):
        if (eeprom_index == 0):
            data[MICRO_CODES[i].micro_code_bits] = (MICRO_CODES[i].control_line_bits ^ INVERTED_LOGIC_MASK) & 0b11111111
        elif (eeprom_index == 1):
            data[MICRO_CODES[i].micro_code_bits] = (MICRO_CODES[i].control_line_bits ^ INVERTED_LOGIC_MASK) >> 8
    return bytes(data)

def generate_data_for_digits_display_decoder_eeprom() -> bytes:
    data = bytearray(EEPROM_SIZE_IN_BYTES)
    for number in range(-128, 128):
        number_as_byte = number & 0b11111111
        for digit_index in range(3):
            if (((number == 0) and (digit_index == 0)) or (int(number / (10 ** digit_index)) != 0)):
                data[digit_index | (number_as_byte << 2)] = convert_digit_to_7_segments_bits(int(abs(number) / (10 ** digit_index)) % 10)
        if (number < 0):
            data[3 | (number_as_byte << 2)] = 0b01000000
    return bytes(data)



with open("ID0_EEPROM", "wb") as file:
    file.write(generate_data_for_instruction_decoder_eeprom(0))
with open("ID1_EEPROM", "wb") as file:
    file.write(generate_data_for_instruction_decoder_eeprom(1))
with open("DDD_EEPROM", "wb") as file:
    file.write(generate_data_for_digits_display_decoder_eeprom())
