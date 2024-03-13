# REGISTERS
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

instruction = {
    
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
    
    # S-type
    "sw": ("0100011", "010"),
    
    # B-type
    "beq": ("1100011", "000"),
    "bne": ("1100011", "001"),
    "blt": ("1100011", "100"),
    "bge": ("1100011", "101"),
    "bltu": ("1100011", "110"),
    "bgeu": ("1100011", "111"),
    
    # U-type
    "lui": ("0110111"),
    "auipc": ("0010111"),
    
    # J-type
    "jal": ("1101111")
}

Rtype =["add","sub","sll",",slt","sltu","xor","srl","or","and"]
Itype=["lw","addi","sltiu","jalr"]
Stype=["sw"]
Btype=["blt","bge","bltu","bgeu","bne","beq"]
Utype=["auipc","lui"]
Jtype=["jal"]
all_type=Rtype+Itype+Stype+Btype+Utype+Jtype

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

def typo_inst(inst):   
    if(inst not in all_type):
            print("Error in instruction name ", inst) 
            return False   
    return True
    
def typo_reg(reg):
    if(reg not in regdict.keys()):
            print("Error in register name ", reg)
            return False
    return True

# retrun error if not even a single halt instruction is present
def missing_halt(all_inst):
    halt = ["beq", "zero", "zero", "0"]
    for i in all_inst:
        if all_inst[i] == halt:
            return True
    print("Error: missing halt instruction")
    return False

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
    new_dec=int(decimal_num)
    if new_dec < 0:
        new_dec += 2 ** num_bits

    binary = bin(new_dec)[2:].zfill(num_bits)
    return binary
 
def typeR(ins,rd,rs1,rs2):
    if(typo_reg(rd) is True and typo_reg(rs1) is True and typo_reg(rs2) is True):
        if(typo_inst(ins)):
            print(instruction[ins][2]+regdict[rs2]+regdict[rs1]+instruction[ins][1]+regdict[rd]+instruction[ins][0])
        else:
            exit()
    else:
        exit()

def typeI(ins,rd,rs1,imm):
    k=dec_to_bin_12(imm)
    if(typo_reg(rd) is True and typo_reg(rs1) is True):
        if(typo_inst(ins)):
            print(k+regdict[rs1]+instruction[ins][1]+regdict[rd]+instruction[ins][0])
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
            print(y,regdict[rd],regdict[rs1],instruction[ins][1],x,instruction[ins][0])
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
            print(bin,regdict[rd],instruction[ins][0])
        else:
            exit()
    else:
        exit()
               
def outofbounds(inst,imm):
    if(inst in Utype or inst in Jtype):
        if(len(imm)>12):
            print("immediate out of bounds")
            return False
        return True
    else:
        if(len(imm)>20):
            print("immediate out of bounds")
            return False
        return True
   
def line(pc):
    if(pc>64):
        print("Line count exceeded 64")
        return False
    return True

import os
import sys
if len(sys.argv) != 2:
    print("Usage: python script.py folder_path")
    sys.exit(1)

# Get the folder path from the command-line argument
folder_path = sys.argv[1]


# List all files in the folder
files = os.listdir(folder_path)

# Iterate over each file in the folder
for file_name in files:
    # Construct the full path of the file
    file_path = os.path.join(folder_path, file_name)
    instruct = parseForInstructions(file_path)
    labels = get_labels(file_path)
    print(instruct)
    print(labels)
    for i in instruct:
        if(instruct[i][0] in Rtype):
            typeR(instruct[i][0],instruct[i][1],instruct[i][2],instruct[i][3])
        elif(instruct[i][0] in Itype):
            if(len(instruct[i])==4):
                typeI(instruct[i][0],instruct[i][1],instruct[i][2],instruct[i][3])
            else:
                k=instruct[i][2].split('(')
                typeI(instruct[i][0],instruct[i][1],k[1][0:-1],k[0])
        elif(instruct[i][0] in Stype):
            typeS(instruct[i][0],instruct[i][1],instruct[i][2],instruct[i][3])
        elif(instruct[i][0] in Utype):
            typeU(instruct[i][0],instruct[i][1],instruct[i][2])




