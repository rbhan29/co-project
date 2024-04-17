import sys

# Name of Registers
reg_file = {
    "00000": "zero",
    "00001": "ra",
    "00010": "sp",
    "00011": "gp",
    "00100": "tp",
    "00101": "t0",
    "00110": "t1",
    "00111": "t2",
    "01000": "s0",
    "01001": "s1",
    "01010": "a0",
    "01011": "a1",
    "01100": "a2",
    "01101": "a3",
    "01110": "a4",
    "01111": "a5",
    "10000": "a6",
    "10001": "a7",
    "10010": "s2",
    "10011": "s3",
    "10100": "s4",
    "10101": "s5",
    "10110": "s6",
    "10111": "s7",
    "11000": "s8",
    "11001": "s9",
    "11010": "s10",
    "11011": "s11",
    "11100": "t3",
    "11101": "t4",
    "11110": "t5",
    "11111": "t6",
}

# Register Values
register_val = {
    "00000": 0,
    "00001": 0,
    "00010": 0x0000_0100,
    "00011": 0,
    "00100": 0,
    "00101": 0,
    "00110": 0,
    "00111": 0,
    "01000": 0,
    "01001": 0,
    "01010": 0,
    "01011": 0,
    "01100": 0,
    "01101": 0,
    "01110": 0,
    "01111": 0,
    "10000": 0,
    "10001": 0,
    "10010": 0,
    "10011": 0,
    "10100": 0,
    "10101": 0,
    "10110": 0,
    "10111": 0,
    "11000": 0,
    "11001": 0,
    "11010": 0,
    "11011": 0,
    "11100": 0,
    "11101": 0,
    "11110": 0,
    "11111": 0,
}

# Opcodes
R_type = ["0110011"]
I_type = ["0000011", "0010011", "1100111"]
S_type = ["0100011"]
B_type = ["1100011"]
U_type = ["0110111", "0010111"]
J_type = ["1101111"]

# Data-Memory
data_memory = {0x0001_0000 + 4 * i: 0 for i in range(32)}

def regwrite(reg, value):
    if reg != "00000":
        register_val[reg] = value


def sext(binary, num_bits):
    if binary[0] == "1":
        return "1" * (num_bits - len(binary)) + binary
    else:
        return "0" * (num_bits - len(binary)) + binary


def dec_to_twocomp(decimal_num, num_bits):
    new_dec = int(decimal_num)
    if new_dec < 0:
        new_dec += 2**num_bits

    binary = bin(new_dec)[2:].zfill(num_bits)
    return binary


def twocomp_to_dec(binary):
    if binary[0] == "1":
        return -1 * (2**len(binary) - int(binary, 2))
    else:
        return int(binary, 2)


def unsigned(val):
    if val >= 0:
        return val
    else:
        return 2**32 + val


def instructions(instruction):
    opcode = instruction[-7:]

    if opcode in R_type:
        return {
            "type": "R",
            "rs1": instruction[-20:-15],
            "rs2": instruction[-25:-20],
            "rd": instruction[-12:-7],
            "funct3": instruction[-15:-12],
            "funct7": instruction[:7],
            "opcode": opcode
        }

    elif opcode in I_type:
        return {
            "type": "I",
            "rs1": instruction[-20:-15],
            "rd": instruction[-12:-7],
            "imm": instruction[0:12],
            "funct3": instruction[-15:-12],
            "opcode": opcode
        }

    elif opcode in S_type:
        return {
            "type": "S",
            "rs1": instruction[-20:-15],
            "rs2": instruction[-25:-20],
            "imm": instruction[0:7] + instruction[-12:-7],
            "funct3": instruction[-15:-12],
            "opcode": opcode
        }

    elif opcode in B_type:
        return {
            "type": "B",
            "rs1": instruction[-20:-15],
            "rs2": instruction[-25:-20],
            "imm": instruction[0] + instruction[-8] + instruction[1:7] + instruction[-12:-8] + '0',
            "funct3": instruction[-15:-12],
            "opcode": opcode
        }

    elif opcode in U_type:
        return {
            "type": "U",
            "rd": instruction[-12:-7],
            "imm": instruction[0:20],
            "opcode": opcode
        }

    elif opcode in J_type:
        return {
            "type": "J",
            "rd": instruction[-12:-7],
            "imm": instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0',
            "opcode": opcode
        }
        # R-type
def add(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 + rs2
    regwrite(instr["rd"], rd)


def sub(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 - rs2
    regwrite(instr["rd"], rd)


def slt(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = 1 if rs1 < rs2 else 0
    regwrite(instr["rd"], rd)


def sltu(instr):
    rs1 = unsigned(register_val[instr["rs1"]])
    rs2 = unsigned(register_val[instr["rs2"]])
    rd = 1 if rs1 < rs2 else 0
    regwrite(instr["rd"], rd)


def xor(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 ^ rs2
    regwrite(instr["rd"], rd)


def and_(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 & rs2
    regwrite(instr["rd"], rd)


def or_(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 | rs2
    regwrite(instr["rd"], rd)


def sll(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 << (rs2 & 0b11111)
    regwrite(instr["rd"], rd)


def srl(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    rd = rs1 >> (rs2 & 0b11111)
    regwrite(instr["rd"], rd)

# S-type
def sw(instr):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    imm = int(instr["imm"], 2)
    addr = rs1 + imm
    data_memory[addr] = rs2

# I-type
def lw(instr):
    rs1 = register_val[instr["rs1"]]
    imm = int(instr["imm"], 2)
    addr = rs1 + imm
    regwrite(instr["rd"], data_memory[addr])


def addi(instr):
    rs1 = register_val[instr["rs1"]]
    imm = twocomp_to_dec(instr["imm"])
    rd = rs1 + imm
    regwrite(instr["rd"], rd)


def sltiu(instr):
    rs1 = unsigned(register_val[instr["rs1"]])
    imm = int(instr["imm"], 2)
    rd = 1 if rs1 < imm else 0
    regwrite(instr["rd"], rd)


def jalr(instr, pc):
    rs1 = register_val[instr["rs1"]] // 4
    imm = twocomp_to_dec(instr["imm"]) // 4
    regwrite(instr["rd"], pc + 1)
    return rs1 + imm

# B-type
def beq(instr, pc):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    if rs1 == rs2:
        return pc + twocomp_to_dec(instr["imm"]) // 4
    else:
        return pc + 1


def bne(instr, pc):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    if rs1 != rs2:
        return pc + twocomp_to_dec(instr["imm"]) // 4
    else:
        return pc + 1


def blt(instr, pc):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    if rs1 < rs2:
        return pc + twocomp_to_dec(instr["imm"]) // 4
    else:
        return pc + 1


def bge(instr, pc):
    rs1 = register_val[instr["rs1"]]
    rs2 = register_val[instr["rs2"]]
    if rs1 >= rs2:
        return pc + twocomp_to_dec(instr["imm"]) // 4
    else:
        return pc + 1


def bltu(instr, pc):
    rs1 = unsigned(register_val[instr["rs1"]])
    rs2 = unsigned(register_val[instr["rs2"]])
    if rs1 < rs2:
        return pc + twocomp_to_dec(instr["imm"]) // 4
    else:
        return pc + 1


def bgeu(instr, pc):
    rs1 = unsigned(register_val[instr["rs1"]])
    rs2 = unsigned(register_val[instr["rs2"]])
    if rs1 >= rs2:
        return pc + twocomp_to_dec(instr["imm"]) // 4
    else:
        return pc + 1

# U-type
def auipc(instr, pc):
    imm = twocomp_to_dec(instr["imm"]) << 12
    regwrite(instr["rd"], pc * 4 + imm)


def lui(instr):
    imm = twocomp_to_dec(instr["imm"]) << 12
    regwrite(instr["rd"], imm)

# J-type
def jal(instr, pc):
    imm = twocomp_to_dec(instr["imm"]) // 4
    regwrite(instr["rd"], (pc + 1) * 4)
    return pc + imm

