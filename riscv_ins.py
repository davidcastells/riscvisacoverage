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
                      'CSRRWI','CSRRSI','CSRRCI',
                      # I add privileged instructions here
                      'URET', 'SRET', 'MRET', 'WFI', 'SFENCE.VMA'
                      ]

rv32m_instructions = ['MUL','MULH','MULHSU','MULHU','DIV','DIVU','REM','REMU']  

rv32f_instructions = ['FLW','FSW','FMADD.S','FMSUB.S','FNMSUB.S','FNMADD.S',
                      'FADD.S','FSUB.S','FMUL.S','FDIV.S','FSQRT.S','FSGNJ.S',
                      'FSGNJN.S','FSGNJX.S','FMIN.S','FMAX.S','FCVT.W.S',
                      'FCVT.WU.S','FMV.X.W','FEQ.S','FLT.S','FLE.S','FCLASS.S',
                      'FCVT.S.W','FCVT.S.WU','FMV.W.X']

rv32d_instructions = ['FLD', 'FSD', 'FMADD.D', 'FMSUB.D', 'FNMSUB.D', 'FNMADD.D',
                      'FADD.D', 'FSUB.D', 'FMUL.D', 'FDIV.D', 'FSQRT.D', 'FSGNJ.D',
                      'FSGNJN.D', 'FSGNJX.D', 'FMIN.D', 'FMAX.D', 'FCVT.S.D',
                      'FCVT.D.S', 'FEQ.D', 'FLT.D', 'FLE.D', 'FCLASS.D', 'FCVT.W.D',
                      'FCVT.WU.D', 'FCVT.D.W', 'FCVT.D.WU' ]

rv32a_instructions = ['LR.W','SC.W','AMOSWAP.W','AMOADD.W','AMOXOR.W','AMOAND.W','AMOOR.W','AMOMIN.W','AMOMAX.W','AMOMINU.W','AMOMAXU.W']
        
    
# 'SLLI','SRLI' appear in the table for RV64I, but are already part of RV32I
rv64i_instructions = ['LWU','LD','SD','ADDIW','SLLIW','SRLIW','SRAIW','ADDW','SUBW','SLLW','SRLW','SRAW']

rv64m_instructions = ['MULW', 'DIVW', 'DIVUW', 'REMW', 'REMUW']

rv64f_instructions = ['FCVT.L.S','FCVT.LU.S','FCVT.S.L','FCVT.S.LU']

rv64a_instructions = ['LR.D','SC.D','AMOSWAP.D','AMOADD.D','AMOXOR.D','AMOAND.D','AMOOR.D','AMOMIN.D','AMOMAX.D','AMOMINU.D','AMOMAXU.D',]

rvc_instructions = ['C.ADDI4SPN', 'C.FLD', 'C.LQ', 'C.LW', 'C.FLW', 'C.LD', 'C.FSD', 'C.SQ', 'C.SW', 'C.FSW', 'C.SD',
                    'C.NOP', 'C.ADDI', 'C.JAL', 'C.ADDIW', 'C.LI', 'C.ADDI16SP', 'C.LUI', 'C.SRLI', 'C.SRLI64', 'C.SRAI', 
                    'C.SRAI64', 'C.ANDI', 'C.SUB', 'C.XOR', 'C.OR', 'C.AND', 'C.SUBW', 'C.ADDW',
                    'C.J', 'C.BEQZ', 'C.BNEZ', 'C.SLLI', 'C.SLLI64', 'C.FLDSP', 'C.LQSP', 'C.LWSP',
                    'C.FLWSP', 'C.LDSP', 'C.JR', 'C.MV', 'C.EBREAK', 'C.JALR', 'C.ADD', 'C.FSDSP',
                    'C.SQSP', 'C.SWSP', 'C.FSWSP', 'C.SDSP']
    
def _isCompactIns(ins):
    opcode_c = ins & 0x03
    if (opcode_c == 0x03):
        return False
    return True

def ins_to_str(ins, isa=32):
    ins16 = ins & 0xFFFF
    opcode_c = ins & 0x03
    opcode = ins & 0x7F
    func2 = (ins >> 25) & 0x3
    func3 = (ins >> 12) & 0x7
    func3_c = (ins >> 13) & 0x7
    func5 = (ins >> 27) & 0x1F
    func6 = (ins >> 26) & 0x3F
    func7 = (ins >> 25) & 0x7F
    rs2 = (ins >> 20) & 0x1F
    rd5_c = (ins >> 7) & 0x1F
    rdu2_c = (ins >> 10) & 0x03
    r2u2_c = (ins >> 5) & 0x03
    r25_c = (ins >> 5) & 0x1F
    imm1_c = ((ins >> 12) & 0x1) 
    imm5_c = (((ins >> 12) & 0x1) << 5) | ((ins >> 2) & 0x1F)
    imm3_c = (((ins >> 12) & 0x1) << 2) | ((ins >> 5) & 0x03)
    
    if (opcode_c == 0x00):
        if (func3_c == 0x00):
            return 'C.ADDI4SPN'
        if (func3_c == 0x01):
            if (isa == 128):
                return 'C.LQ'
            return 'C.FLD' 
        if (func3_c == 0x02):
            return 'C.LW'
        if (func3_c == 0x03):
            if (isa == 128):
                return 'C.LD'
            return 'C.FLW' 
        if (func3_c == 0x05):
            if (isa == 128):
                return 'C.SQ'
            return 'C.FSD' 
        if (func3_c == 0x06):
            return 'C.SW'
        if (func3_c == 0x07):
            if (isa == 128):
                return 'C.SD'
            return 'C.FSW' 
        
    if (opcode_c == 0x01):
        if (ins16 == 0x00):
            return 'C.NOP'
        if (func3_c == 0x00):
            return 'C.ADDI'
        if (func3_c == 0x01):
            if (isa == 32):
                return 'C.JAL'
            return 'C.ADDIW'
        if (func3_c == 0x02):
            return 'C.LI'
        if (func3_c == 0x03):
             if (rd5_c == 0x02):
                 return 'C.ADDI16SP'
             else:
                 return 'C.LUI'             
        if (func3_c == 0x04):
            if (rdu2_c == 0x00):
                if (imm5_c == 0x00):
                    return 'C.SRLI64'
                else:
                    return 'C.SRLI' 
            if (rdu2_c == 0x01):
                if (imm5_c == 0x00):
                    return 'C.SRAI64'
                else:
                    return 'C.SRAI'
            if (rdu2_c == 0x02):
                return 'C.ANDI'
            if (rdu2_c == 0x03):
                if (imm3_c == 0x00):
                    return 'C.SUB'
                if (imm3_c == 0x01):
                    return 'C.XOR'
                if (imm3_c == 0x02):
                    return 'C.OR'
                if (imm3_c == 0x03):
                    return 'C.AND'
                if (imm3_c == 0x04):
                    return 'C.SUBW'
                if (imm3_c == 0x05):
                    return 'C.ADDW'
        if (func3_c == 0x05):
            return 'C.J'
        if (func3_c == 0x06):
            return 'C.BEQZ'
        if (func3_c == 0x07):
            return 'C.BNEZ'
    
    if (opcode_c == 0x02):
        if (func3_c == 0x00):
            if (imm5_c == 0x00):
                return 'C.SLLI64'
            else:
                return 'C.SLLI'
        if (func3_c == 0x01):
            if (isa == 128):
                return 'C.LQSP'
            return 'C.FLDSP' 
        if (func3_c == 0x02):
            return 'C.LWSP' 
        if (func3_c == 0x03):
            if (isa == 32):
                return 'C.FLWSP'
            return 'C.LDSP'
        if (func3_c == 0x04):
            if (imm5_c == 0x00):
                return 'C.JR'
            if (imm1_c == 0x00):
                return 'C.MV'
            if (imm1_c == 0x01):
                if (rd5_c == 0x00):
                    return 'C.EBREAK'
                if (r25_c == 0x00):
                    return 'C.JALR'
                else:
                    return 'C.ADD'
        if (func3_c == 0x05):
            if (isa == 128):
                return 'C.SQSP'
            return 'C.FSDSP' 
        if (func3_c == 0x06):
            return 'C.SWSP'
        if (func3_c == 0x07):
            if (isa == 32):
                return 'C.FSWSP'
            return 'C.SDSP'
        
    if (opcode == 0x03):
        if (func3 == 0x00):
            return 'LB'
        if (func3 == 0x01):
            return 'LH'
        if (func3 == 0x02):
            return 'LW'
        if (func3 == 0x03):
            return 'LD'
        if (func3 == 0x04):
            return 'LBU'
        if (func3 == 0x05):
            return 'LHU'
        if (func3 == 0x06):
            return 'LWU'
        
    if (opcode == 0x07):
        if (func3 == 0x02):
            return 'FLW'
        if (func3 == 0x03):
            return 'FLD'
    
    if (opcode == 0b0001111):
        if (func3 == 0b000):
            return 'FENCE'
        if (func3 == 0b001):
            return 'FENCE.I'
        
    if (opcode == 0x13):
        if (func3 == 0x00):
            return 'ADDI'
        if (func3 == 0x01):
            if (func6 == 0x00):
                return 'SLLI'

        if (func3 == 0x02):
            return 'SLTI'
        if (func3 == 0x03):
            return 'SLTIU'
        if (func3 == 0x04):
            return 'XORI'
        if (func3 == 0x05):
            if (func6 == 0x00):
                return 'SRLI'
            if (func6 == 0x10):
                return 'SRAI'
        if (func3 == 0x06):
            return 'ORI'
        if (func3 == 0x07):
            return 'ANDI'

    if (opcode == 0x17):
        return 'AUIPC'

    if (opcode == 0x1b):
        if (func3 == 0x00):
            return 'ADDIW'
        if (func3 == 0x01):
            if (func7 == 0x00):
                return 'SLLIW'
        if (func3 == 0x05):
            if (func7 == 0x00):
                return 'SRLIW'
            if (func7 == 0x20):
                return 'SRAIW'

    if (opcode == 0x23):
        if (func3 == 0x00):
            return 'SB'
        if (func3 == 0x01):
            return 'SH'
        if (func3 == 0x02):
            return 'SW'
        if (func3 == 0x03):
            return 'SD'

    if (opcode == 0x27):
        if (func3 == 0x02):
            return 'FSW'
        if (func3 == 0x03):
            return 'FSD'

    if (opcode == 0b0101111):
        if (func3 == 0b010):
            if (func5 == 0b00000):
                return 'AMOADD.W'
            if (func5 == 0b00001):
                return 'AMOSWAP.W'
            if (func5 == 0b00010):
                return 'LR.W'
            if (func5 == 0b00011):
                return 'SC.W'
            if (func5 == 0b00100):
                return 'AMOXOR.W'
            if (func5 == 0b01000):
                return 'AMOOR.W'
            if (func5 == 0b01100):
                return 'AMOAND.W'
            if (func5 == 0b10000):
                return 'AMOMIN.W'
            if (func5 == 0b10100):
                return 'AMOMAX.W'
            if (func5 == 0b11000):
                return 'AMOMINU.W'
            if (func5 == 0b11100):
                return 'AMOMAXU.W'
        if (func3 == 0b011):
            if (func5 == 0b00010):
                return 'LR.D'
            if (func5 == 0b00011):
                return 'SC.D'
            if (func5 == 0b00001):
                return 'AMOSWAP.D'
            if (func5 == 0b00000):
                return 'AMOADD.D'
            if (func5 == 0b00100):
                return 'AMOXOR.D'
            if (func5 == 0b01100):
                return 'AMOAND.D'
            if (func5 == 0b01000):
                return 'AMOOR.D'
            if (func5 == 0b10000):
                return 'AMOMIN.D'
            if (func5 == 0b10100):
                return 'AMOMAX.D'
            if (func5 == 0b11000):
                return 'AMOMINU.D'
            if (func5 == 0b11100):
                return 'AMOMAXU.D'
            
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
    
    if (opcode == 0x3b):
        if (func3 == 0x00):
            if (func7 == 0x00):
                return 'ADDW'
            if (func7 == 0x01):
                return 'MULW'
            if (func7 == 0x20):
                return 'SUBW'
        if (func3 == 0x01):
            if (func7 == 0x00):
                return 'SLLW'
        if (func3 == 0x04):
            if (func7 == 0x01):
                return 'DIVW'
        if (func3 == 0x05):
            if (func7 == 0x00):
                return 'SRLW'
            if (func7 == 0x01):
                return 'DIVUW'
            if (func7 == 0x20):
                return 'SRAW'
        if (func3 == 0x06):
            if (func7 == 0x01):
                return 'REMW'
        if (func3 == 0x07):
            if (func7 == 0x01):
                return 'REMUW'
    
    if (opcode == 0x43):
        if (func2 == 0x00):
            return 'FMADD.S'
        if (func2 == 0x01):
            return 'FMADD.D'
        
    if (opcode == 0x47):
        if (func2 == 0x00):
            return 'FMSUB.S'
        if (func2 == 0x01):
            return 'FMSUB.D'
        
    if (opcode == 0x4b):
        if (func2 == 0x00):
            return 'FNMSUB.S'
        if (func2 == 0x01):
            return 'FNMSUB.D'
        
    if (opcode == 0x4f):
        if (func2 == 0x00):
            return 'FNMADD.S'
        if (func2 == 0x01):
            return 'FNMADD.D'
        
    if (opcode == 0x53):
        if (func7 == 0x00):
            return 'FADD.S'
        if (func7 == 0x01):
            return 'FADD.D'
        if (func7 == 0x04):
            return 'FSUB.S'
        if (func7 == 0x05):
            return 'FSUB.D'
        if (func7 == 0x08):
            return 'FMUL.S'
        if (func7 == 0x09):
            return 'FMUL.D'
        if (func7 == 0x0c):
            return 'FDIV.S'
        if (func7 == 0x0d):
            return 'FDIV.D'
        if (func7 == 0x10):
            if (func3 == 0x00):
                return 'FSGNJ.S'
            if (func3 == 0x01):
                return 'FSGNJN.S'
            if (func3 == 0x02):
                return 'FSGNJX.S'
        if (func7 == 0x14):
            if (func3 == 0x00):
                return 'FMIN.S'
            if (func3 == 0x01):
                return 'FMAX.S'
        if (func7 == 0x2c):
            if (rs2 == 0x00):
                return 'FSQRT.S'
        if (func7 == 0x2d):
            if (rs2 == 0x00):
                return 'FSQRT.D'
        if (func7 == 0x50):
            if (func3 == 0x02):
                return 'FEQ.S'
            if (func3 == 0x01):
                return 'FLT.S'
            if (func3 == 0x00):
                return 'FLE.S'
        if (func7 == 0x60):
            if (rs2 == 0x00):
                return 'FCVT.W.S'
            if (rs2 == 0x01):
                return 'FCVT.WU.S'
            if (rs2 == 0x02):
                return 'FCVT.L.S'
            if (rs2 == 0x03):
                return 'FCVT.LU.S'
        if (func7 == 0x68):
            if (rs2 == 0x00):
                return 'FCVT.S.W'
            if (rs2 == 0x01):
                return 'FCVT.S.WU'
            if (rs2 == 0x02):
                return 'FCVT.S.L'
            if (rs2 == 0x03):
                return 'FCVT.S.LU'
        if (func7 == 0x70):
            if (rs2 == 0x00):
                if (func3 == 0x00):
                    return 'FMV.X.W'
                if (func3 == 0x01):
                    return 'FCLASS.S'
        if (func7 == 0x78):
            if (rs2 == 0x00):
                if (func3 == 0x00):
                    return 'FMV.W.X'
                
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
    
    if (opcode == 0b1110011):
        if (func3 == 0x00):
            if (ins == 0x00000073):
                return 'ECALL'
            if (ins == 0x00200073):
                return 'URET'
            if (ins == 0x10200073):
                return 'SRET'
            if (ins == 0x10500073):
                return 'WFI'
            if (ins == 0x30200073):
                return 'MRET'
            if (ins == 0x00100073):
                return 'EBREAK'
            if (func7 == 0b0001001):
                return 'SFENCE.VMA'
        if (func3 == 0x01):
            return 'CSRRW'
        if (func3 == 0x02):
            return 'CSRRS'
        if (func3 == 0x03):
            return 'CSRRC'
        if (func3 == 0x05):
            return 'CSRRWI'
        if (func3 == 0x06):
            return 'CSRRSI'
        if (func3 == 0x07):
            return 'CSRRCI'
        
    #return 'Unknown opcode {:x} func3 {:x} func7 {:x} full {:08x}'.format(opcode, func3, func7, ins)
    if (_isCompactIns(ins)):
        raise Exception('Unknown opcode {:02b} func3 {:03b}  full {:08x}'.format(opcode_c, func3_c,  ins))
    else:
        raise Exception('Unknown opcode {:07b} func3 {:03b} func7 {:x} full {:08x}'.format(opcode, func3, func7, ins))
    
RTypeIns = ['ADD','SUB','SLL','SLT','SLTU','XOR','SRL','SRA','OR','AND']
ITypeIns = ['JALR','LB','LH','LW','LBU','LHU','ADDI','SLTI','SLTIU','XORI',
            'ORI','ANDI','SLLI','SRLI','SRAI']
STypeIns = ['SB','SH','SW']
BTypeIns = ['BEQ','BNE','BLT','BGE','BLTU','BGEU']
UTypeIns = ['LUI','AUIPC']
JTypeIns = ['JAL']
CSRRIns   = ['CSRRW','CSRRS','CSRRC']
CSRIIns   = ['CSRRWI','CSRRSI','CSRRCI']

CRIns = []
CIIns = []
CSSIns = []
CIWIns = []
CLIns = []
CSIns = []
CBIns = []
CJIns = []

def ins_to_regs(ins, isa):
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
    
def get_ins(code, isa):
    """
    Return the sequence of instructions from the code

    Parameters
    ----------
    code : TYPE
        DESCRIPTION.
    isa : int
        32, 64, or 128

    Returns
    -------
    ret : TYPE
        DESCRIPTION.

    """
    size = len(code)
    off = 0    
    
    ret = []
    
    while (off <= (size-4)):
        try:
        #if (True):
            cins = int.from_bytes(code[off:off+2], byteorder='little')
            
            if (_isCompactIns(cins)):
                ins = cins
                #print('{:08X} - {:08X}'.format(off, ins))
                off += 2

            else:
                ins = int.from_bytes(code[off:off+4], byteorder='little')
                #print('{:08X} - {:08X}'.format(off, ins))
                off += 4

            ret.append(ins_to_str(ins, isa))

        except:
            print('{:08X} - unable to decode instruction {:08X} - {:08b} {:08b} {:08b} {:08b}'.format(off, ins, (ins>>24)&0xFF, (ins>>16)&0xFF, (ins>>8)&0xFF, ins&0xFF))
            import sys
            sys.exit()
                

    return ret

def get_regs(code, isa):
    size = len(code)
    off = 0    
    
    ret = set([])
    
    while (off <= (size-4)):
        cins = int.from_bytes(code[off:off+2], byteorder='little')
        
        if (_isCompactIns(cins)):
            ins = cins
            #print('{:08X} - {:08X}'.format(off, ins))
            off += 2

        else:
            ins = int.from_bytes(code[off:off+4], byteorder='little')
            #print('{:08X} - {:08X}'.format(off, ins))
            off += 4
    
        regs = ins_to_regs(ins, isa)

        
        #print('reg {:x}'.format(off))
        
        if not(regs is None):
            for r in regs:
                ret.add(r)

        
        
        #print('Regs so far', ret)


    return ret