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
        


def typeI(ins,rd,immrs1):
    imm,rs1=immrs1.split("(")
    print(imm,rs1)
    k=dec_to_bin_12(imm)
    if(typo_reg(rd) is True and typo_reg(rs1) is True):
        if(typo_inst(ins)):
            print(k+reg_file[rs1]+instruction[ins][1]+reg_file[rd]+instruction[ins][0])
        else:
            exit()      
    else:
        exit()


def typeB(ins, rs1, rs2, lbl,pc):

    if ins=="beq" and rs1=="zero" and rs2=="zero" and lbl=="0":
        print("00000000000000000000000001100011")
        return
    # getting the line number of the label
    lbl_pc = labels[lbl]
    # getting the current line number of the instruction
    current_pc = pc
    # calculating the offset
    offset = (current_pc-lbl_pc) * 4

    imm = decimal_to_binary_twos_complement(offset,20)[7:19]
    w = imm[0]
    x = imm[2:8]
    y = imm[8::]
    z = imm[1]

    if typo_reg(rs1) is True and typo_reg(rs2) is True:
        if typo_inst(ins):
            print(
                str(w)
                + str(x)
                + reg_file[rs2]
                + reg_file[rs1]
                + instruction[ins][1]
                + str(y)
                + str(z)
                + instruction[ins][0]
            )
        else:
            exit()
    else:
        exit()
    
def typeJ(ins, rd, lbl,pc):
    print(isinstance(lbl, int))
    if lbl in labels:
        lbl_pc = labels[lbl]
        # getting the current line number of the instruction
        current_pc = pc
        # calculating the offset
        offset = (current_pc-lbl_pc) * 4        
        imm = decimal_to_binary_twos_complement(offset,32)[-2:-22:-1][-1::-1]
        print(imm)

        w = imm[0]
        x = imm[-1:-11:-1][-1::-1]
        y = imm[-11]
        z = imm[1:9]

        if typo_reg(rd) is True:
            if typo_inst(ins):
                print(
                    str(w)
                    + str(x)
                    + str(y)
                    + str(z)
                    + reg_file[rd]
                    + instruction[ins]
                )
    elif isinstance(lbl, int):
        imm = decimal_to_binary_twos_complement(lbl,32)[-2:-22:-1][-1::-1]
        w = imm[0]
        x = imm[-1:-11:-1][-1::-1]
        y = imm[-11]
        z = imm[1:9]
        print(imm)
        if typo_reg(rd) is True:
            if typo_inst(ins):
                print(
                    str(w)
                    + str(x)
                    + str(y)
                    + str(z)
                    + reg_file[rd]
                    + instruction[ins]
                )
    else:
        print("Error: label not found")
        exit()
    

    
    
    
def outofbounds(inst,imm):
    if(inst in type_U or inst in type_J):
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

file_path = r"C:\Users\adity\Desktop\IIITD\1-2\CO\CO Project evaluation framework\automatedTesting\tests\assembly\simpleBin\test1.txt"

all_inst = parseForInstructions(file_path)
labels = get_labels(file_path)
print(all_inst)
print(labels)

for i in all_inst:
    if all_inst[i][0] in type_R:
        typeR(all_inst[i][0], all_inst[i][1], all_inst[i][2], all_inst[i][3])
    elif all_inst[i][0] in type_I:
        typeI(all_inst[i][0], all_inst[i][1], all_inst[i][2], all_inst[i][3])
    elif all_inst[i][0] in type_S:
        typeS(all_inst[i][0], all_inst[i][1], all_inst[i][2], all_inst[i][3])
    elif all_inst[i][0] in type_B:
        typeB(all_inst[i][0], all_inst[i][1], all_inst[i][2], all_inst[i][3],i)
    elif all_inst[i][0] in type_U:
        typeU(all_inst[i][0], all_inst[i][1], all_inst[i][2])
    elif all_inst[i][0] in type_J:
        typeJ(all_inst[i][0], all_inst[i][1], all_inst[i][2],i)
    else:
        print("Error: Instruction not found")
        exit()
    if outofbounds(all_inst[i][0],all_inst[i][3]) is False:
        exit()
    if line(i) is False:
        exit()
    if missing_halt(all_inst) is False:
        exit()
