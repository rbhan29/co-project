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


def missing_halt(all_inst):
    halt = ["beq", "zero", "zero", "0"]
    for i in all_inst:
        if all_inst[i] == halt:
            return True
    print("Error: missing halt Instruction")
    return False
    def parseForInstructions(file):
    instructions = {}

    with open(file, "r") as f:

        lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = [x for x in lines if x]
        lines = [x.replace(",", " ") for x in lines]

        line_count = 0
        for i in lines:
            if i.split()[0].endswith(":"):
                instructions[line_count] = i.split()[1:]
            else:
                instructions[line_count] = i.split()
            line_count += 1

    return instructions


def get_labels(file):
    labels = {}

    with open(file, "r") as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = [x for x in lines if x]
        lines = [x.replace(",", " ") for x in lines]
        line_count = 0
        for i in lines:
            if i.split()[0].endswith(":"):
                labels[i.split()[0][0:-1]] = line_count
            line_count += 1

    return labels

    
def dec_to_twocomp(decimal, bits):
    if decimal < 0:
        decimal = (1<<bits) + decimal
    format_string = '{:0%ib}' % bits
    return format_string.format(decimal)
    

def dec_to_bin_12(decimal):
    binary = bin(int(decimal))[2:] 
    binary = binary.zfill(12)
    return binary

def dec_to_bin_20(decimal):
    binary = bin(int(decimal))[2:] 
    binary = binary.zfill(20)
    return binary

def decimal_to_binary_twos_complement(decimal_num, num_bits):
    # Handle negative numbers
    if decimal_num < 0:
        decimal_num += 2 ** num_bits

    binary = bin(decimal_num)[2:].zfill(num_bits)
    return binary

def typeR(ins,rd,rs1,rs2):
    if(typo_reg(rd) is True and typo_reg(rs1) is True and typo_reg(rs2) is True):
        if(typo_inst(ins)):
            print(instruction[ins][2]+reg_file[rs2]+reg_file[rs1]+instruction[ins][1]+reg_file[rd]+instruction[ins][0])
        else:
            exit()
    else:
        exit()
        
def typeS(ins,rd,imm,rs1):
    bin = dec_to_bin_12(imm)
    x = bin[0:5][::-1]
    y = bin[6:12][::-1]
    if(typo_reg(rd) is True and typo_reg(rs1) is True ):
        if(typo_inst(ins)):
            print(y,reg_file[rd],reg_file[rs1],instruction[ins][1],x,instruction[ins][0])
        else:
            exit()
    else:
        exit()
        
def typeU(ins,rd,imm):
    bin = decimal_to_binary_twos_complement(imm, 32)
    bin = bin[::-1]
    bin = bin[12:32]
    
    if(typo_reg(rd) is True):
        if(typo_inst(ins)):
            print(bin,reg_file[rd],instruction[ins][0])
        else:
            exit()
    else:
        exit()




