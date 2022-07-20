# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 10:28:14 2022

@author: dcr
"""

rv32i_instructions = ['LUI','AUIPC','JAL','JALR','BEQ','BNE','BLT','BGE','BLTU', 
                      'BGEU','LB','LH','LW','LBU','LHU','SB','SH','SW','ADDI',
                      'SLTI','SLTIU','XORI','ORI','ANDI','SLLI','SRLI','SRAI',
                      'ADD','SUB','SLL','SLT','SLTU','XOR','SRL','SRA','OR','AND',
                      'FENCE', 'FENCE.I','ECALL','EBREAK','CSRRW','CSRRS','CSRRC',
                      'CSRRWI','CSRRSI','CSRRCI']

rv32m_instructions = ['MUL','MULH','MULHSU','MULHU','DIV','DIVU','REM','REMU']  
    
def ins_to_str(ins):
    opcode = ins & 0x7F
    func3 = (ins >> 12) & 0x7
    func7 = (ins >> 25) & 0x7F
    
    if (opcode == 0x03):
        if (func3 == 0x00):
            return 'LB'
        if (func3 == 0x01):
            return 'LH'
        if (func3 == 0x02):
            return 'LW'
        if (func3 == 0x04):
            return 'LBU'
        if (func3 == 0x05):
            return 'LHU'
    if (opcode == 0x13):
        if (func3 == 0x00):
            return 'ADDI'
        if (func3 == 0x01):
            if (func7 == 0x00):
                return 'SLLI'
        if (func3 == 0x02):
            return 'SLTI'
        if (func3 == 0x03):
            return 'SLTIU'
        if (func3 == 0x04):
            return 'XORI'
        if (func3 == 0x05):
            if (func7 == 0x00):
                return 'SRLI'
            if (func7 == 0x20):
                return 'SRAI'
        if (func3 == 0x06):
            return 'ORI'
        if (func3 == 0x07):
            return 'ANDI'
    if (opcode == 0x17):
        return 'AUIPC'
    if (opcode == 0x23):
        if (func3 == 0x00):
            return 'SB'
        if (func3 == 0x01):
            return 'SH'
        if (func3 == 0x02):
            return 'SW'
        if (func3 == 0x03):
            return 'SD'
    if (opcode == 0x33):
        if (func3 == 0x00):
            if (func7 == 0x00):
                return 'ADD'
            if (func7 == 0x01):
                return 'MUL'
            if (func7 == 0x20):
                return 'SUB'
        if (func3 == 0x01):
            if (func7 == 0x00):
                return 'SLL'
            if (func7 == 0x01):
                return 'MULH'
        if (func3 == 0x02):
            if (func7 == 0x00):
                return 'SLT'
            if (func7 == 0x01):
                return 'MULHSU'
        if (func3 == 0x03):
            if (func7 == 0x00):
                return 'SLTU'
            if (func7 == 0x01):
                return 'MULHU'
        if (func3 == 0x04):
            if (func7 == 0x00):
                return 'XOR'
            if (func7 == 0x01):
                return 'DIV'
        if (func3 == 0x05):
            if (func7 == 0x00):
                return 'SRL'
            if (func7 == 0x01):
                return 'DIVU'
            if (func7 == 0x20):
                return 'SRA'
        if (func3 == 0x06):
            if (func7 == 0x00):
                return 'OR'
            if (func7 == 0x01):
                return 'REM'
        if (func3 == 0x07):
            if (func7 == 0x00):
                return 'AND'
            if (func7 == 0x01):
                return 'REMU'
            
    if (opcode == 0x37):
        return 'LUI'
    if (opcode == 0x63):
        if (func3 == 0x00):
            return 'BEQ'
        if (func3 == 0x01):
            return 'BNE'
        if (func3 == 0x04):
            return 'BLT'
        if (func3 == 0x05):
            return 'BGE'
        if (func3 == 0x06):
            return 'BLTU'
        if (func3 == 0x07):
            return 'BGEU'
    if (opcode == 0x67):
        if (func3 == 0x00):
            return 'JALR'
    if (opcode == 0x6F):
        return 'JAL'
    if (opcode == 0x73):
        if (func3 == 0x00):
            if (ins == 0x00000073):
                return 'ECALL'
            if (ins == 0x00100073):
                return 'EBREAK'
        
    return 'Unknown opcode {:x} func3 {:x} func7 {:x} full {:08x}'.format(opcode, func3, func7, ins)
    
RTypeIns = ['ADD','SUB','SLL','SLT','SLTU','XOR','SRL','SRA','OR','AND']
ITypeIns = ['JALR','LB','LH','LW','LBU','LHU','ADDI','SLTI','SLTIU','XORI',
            'ORI','ANDI','SLLI','SRLI','SRAI']
STypeIns = ['SB','SH','SW']
BTypeIns = ['BEQ','BNE','BLT','BGE','BLTU','BGEU']
UTypeIns = ['LUI','AUIPC']
JTypeIns = ['JAL']
CSRRIns   = ['CSRRW','CSRRS','CSRRC']
CSRIIns   = ['CSRRWI','CSRRSI','CSRRCI']

def ins_to_regs(ins):
    code = ins_to_str(ins)
    
    rd = 'r{}'.format((ins >> 7) & 0x1F)
    rs1 = 'r{}'.format((ins >> 15) & 0x1F)
    rs2 = 'r{}'.format((ins >> 20) & 0x1F)
    
    csr = 'csr{}'.format((ins >> 20) & 0xFFF)
    
    if (code in RTypeIns):
        return [rd, rs1, rs2]
    if (code in RTypeIns):
        return [rd, rs1]
    if (code in STypeIns):
        return [rs1, rs2]
    if (code in BTypeIns):
        return [rs1, rs2]
    if (code in UTypeIns):
        return [rd]
    if (code in JTypeIns):
        return [rd]
    if (code in CSRRIns):
        return [rd, rs1, csr]
    if (code in CSRIIns):
        return [rd, csr]
    
def get_ins(code):

    size = len(code)
    off = 0    
    
    ret = []
    
    while (off <= (size-4)):
        ins = int.from_bytes(code[off:off+4], byteorder='little')
    
        ret.append(ins_to_str(ins))
        off += 4

    return ret

def get_regs(code):
    size = len(code)
    off = 0    
    
    ret = set([])
    
    while (off <= (size-4)):
        ins = int.from_bytes(code[off:off+4], byteorder='little')
    
        regs = ins_to_regs(ins)

        off += 4
        
        #print('reg {:x}'.format(off))
        
        if (regs is None):
            continue
        
        for r in regs:
            ret.add(r)
        
        #print('Regs so far', ret)


    return ret