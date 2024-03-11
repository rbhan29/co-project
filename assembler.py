#  ALL REGISTERS

regdict = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
}

# Instruction = { opname : (opcode, funct3, funct7)}

Instruction = {

    # R-type
    "add": ("0110011", "000", "0000000"),
    "sub": ("0110011", "000", "0100000"),
    "sll": ("0110011", "001", "0000000"),
    "slt": ("0110011", "010", "0000000"),
    "sltu": ("0110011", "011", "0000000"),
    "xor": ("0110011", "100", "0000000"),
    "srl": ("0110011", "101", "0000000"),
    "or": ("0110011", "110", "0000000"),
    "and": ("0110011", "111", "0000000"),

    # I-type
    "lw": ("0000011", "010"),
    "addi": ("0010011", "000"),
    "sltiu": ("0010011", "011"),
    "jalr": ("1100111", "000"),

    # B-type
    "beq": ("1100011", "000"),
    "bne": ("1100011", "001"),
    "blt": ("1100011", "100"),
    "bge": ("1100011", "101"),
    "bltu": ("1100011", "110"),
    "bgeu": ("1100011", "111"),

    # S-type
    "sw": ("0100011", "010"),

    # U-type
    "lui": ("0110111"),
    "auipc": ("0010111"),

    # J-type
    "jal": ("0010111"),
}

Rtype = ["add", "sub", "sll", ",slt", "sltu", "xor", "srl", "or", "and"]
Itype = ["lw", "addi", "sltiu", "jalr"]
Btype = ["blt", "bge", "bltu", "bgeu", "bne", "beq"]
Stype = ["sw"]
Utype = ["auipc", "lui"]
Jtype = ["jal"]
Alltype = Rtype + Itype + Stype + Btype + Utype + Jtype

def outofbounds(inst, imm):
    if inst in Utype or inst in Jtype:
        if len(imm) > 12:
            print("immediate out of bounds")
            return False
        return True
    else:
        if len(imm) > 20:
            print("immediate out of bounds")
            return False
        return True
       
def typo_inst(inst):
    if inst not in Alltype:
        print("Error in Instruction name ", inst)
        return False
    return True

def typo_reg(reg):
    if reg not in regdict.keys():
        print("Error in register name ", reg)
        return False
    return True

# retrun error if not even a single halt Instruction is present
def missing_halt(all_inst):
    halt = ["beq", "zero", "zero", "0"]
    for i in all_inst:
        if all_inst[i] == halt:
            return True
    print("Error: missing halt Instruction")
    return False



