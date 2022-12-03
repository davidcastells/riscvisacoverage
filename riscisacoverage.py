#
# Copyright (C) 2022 Universitat Autonoma de Barcelona - David Castells-Rufas <david.castells@uab.cat>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from elftools.elf.elffile import ELFFile
from datetime import datetime
import riscv_ins

def _create_histogram(ins):
    ret = {}
    for x in ins:
        if x in ret.keys():
            v = ret[x] + 1
        else:
            v = 1
        ret[x] = v
        
    return ret


def _create_ins_table(rv_ins, rv_ins_name, ins):    
    ins_hist = _create_histogram(ins)
    ins_set = set(ins)
    ins_set = set([x for x in ins_set if x in rv_ins])
    
    ret = '<table border="1">'
    ret += '<head><tr><td>Instruction</td><td>Used</td><td>Count</td></tr></head>'

    for test in rv_ins:
        if test in ins_set:
            ret += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(test, 'Yes', ins_hist[test])
        else:
            ret += '<tr><td>{}</td><td></td><td></td></tr>'.format(test)
            
    ret += '</table>'
    
    ret += '<p>{} ISA instructions: {}<br/>'.format(rv_ins_name, len(rv_ins))
    ret += 'Implemented instructions: {} ({:0.2f}\%)</p>'.format(len(ins_set), len(ins_set)*100/len(rv_ins))
    return ret

            
def _create_rv32i_table(ins):    
    return _create_ins_table(riscv_ins.rv32i_instructions, 'RV32I', ins)

def _create_rv32m_table(ins):    
    return _create_ins_table(riscv_ins.rv32m_instructions, 'RV32M', ins)

def _create_rv32f_table(ins):    
    return _create_ins_table(riscv_ins.rv32f_instructions, 'RV32F', ins)

def _create_rv32d_table(ins):    
    return _create_ins_table(riscv_ins.rv32d_instructions, 'RV32D', ins)

def _create_rv32a_table(ins):    
    return _create_ins_table(riscv_ins.rv32a_instructions, 'RV32A', ins)

def _create_rv64i_table(ins):    
    return _create_ins_table(riscv_ins.rv64i_instructions, 'RV64I', ins)

def _create_rv64m_table(ins):    
    return _create_ins_table(riscv_ins.rv64m_instructions, 'RV64M', ins)

def _create_rv64f_table(ins):    
    return _create_ins_table(riscv_ins.rv64f_instructions, 'RV64F', ins)

def _create_rv64a_table(ins):    
    return _create_ins_table(riscv_ins.rv64a_instructions, 'RV64A', ins)

def _create_rvc_table(ins):    
    rvc_ins = riscv_ins.rvc_instructions
    
    ins_hist = _create_histogram(ins)
    ins_set = set(ins)
    ins_set = set([x for x in ins_set if x in rvc_ins])

    
    ret = '<table border="1">'
    ret += '<head><tr><td>Instruction</td><td>Used</td><td>Count</td></tr></head>'

    for test in rvc_ins:
        if test in ins_set:
            ret += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(test, 'Yes', ins_hist[test])
        else:
            ret += '<tr><td>{}</td><td></td><td></td></tr>'.format(test)
            
    ret += '</table>'
    
    ret += '<p>RV6C ISA instructions: {}<br/>'.format(len(rvc_ins))
    ret += 'Implemented instructions: {} ({:0.2f}\%)</p>'.format(len(ins_set), len(ins_set)*100/len(rvc_ins))
    return ret

def _create_registers_table(regs):
    cpu_regs = ['r0','r1','r2','r3','r4','r5','r6','r7',
                'r8','r9','r10','r11','r12','r13','r14','r15',
                'r16', 'r17','r18','r19','r20','r21','r22','r23',
                'r24', 'r25','r26','r27','r28','r29','r30','r31']
    
    ret = '<table border="1">'
    ret += '<head><tr><td>Register</td><td>Used</td></tr></head>'

    for test in cpu_regs:
        if test in regs:
            ret += '<tr><td>{}</td><td>{}</td></tr>'.format(test, 'Yes')
        else:
            ret += '<tr><td>{}</td><td></td></tr>'.format(test)
            
    ret += '</table>'
    
    ret += '<p>RISCV Registers: {}<br/>'.format(len(cpu_regs))
    ret += 'Used Registers: {} ({:0.2f}\%)</p>'.format(len(regs), len(regs)*100/len(cpu_regs))
    return ret

def create_html_report(file, htmlfile, filetype='elf', elfclass=32):
    if (filetype == 'elf'):
        create_html_report_from_elf(file, htmlfile)
    elif (filetype == 'bin'):
        create_html_report_from_bin(file, htmlfile, elfclass)
    else:
        raise Exception('Unsupported file type')

def create_html_report_from_elf(elffilename, htmlfile):
    
    print('ELFFile:', elffilename)
    with open(elffilename, 'rb') as fi:
        elffile = ELFFile(fi)
        
        sectab = '<table>'
        sectab += '<tr><td>Section Name</td></tr>\n'
        
        for section in elffile.iter_sections():
            sectab += '<tr><td>{}</td></tr>\n'.format(section.name)

        sectab += '</table>'
        
        text_section = elffile.get_section_by_name(".text")
        code = text_section.data()
        code_len = len(code)
        
    print('Getting instructions')
    
    ins = riscv_ins.get_ins(code, elffile.elfclass)
    ins_set = set(ins)
    
    print('Getting register usage')
    regs = riscv_ins.get_regs(code, elffile.elfclass)
        
    fo = open(htmlfile, 'w')
    
    fo.write('<html>')
    fo.write('<body>')
    fo.write('<h1>RISC-V ISA Coverage Report for file {} </h1>'.format(elffilename))
    fo.write('<p><small>This report is automatically created by <b>riscisacoverage</b> tool. Check <a href="https://github.com/davidcastells/riscvisacoverage">https://github.com/davidcastells/riscvisacoverage</a> </small></p><br>')
    fo.write('<table>')
    fo.write('<tr><td>File Path:</td><td>{}</td>'.format(elffilename))
    fo.write('<tr><td>Report date:</td><td>{}</td>'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    fo.write('<tr><td>Elf class:</td><td>{}</td>'.format(elffile.elfclass))
    fo.write('<tr><td>Code Length:</td><td>{}</td>'.format(code_len))
    fo.write('</table>')

    fo.write('<table><tr><td valign="top">')
    fo.write('<h2>RV32I</h2>')
    print('Analyzing RV32I instructions')    
    fo.write(_create_rv32i_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32M</h2>')
    print('Analyzing RV32M instructions')    
    fo.write(_create_rv32m_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32F</h2>')
    print('Analyzing RV32F instructions')    
    fo.write(_create_rv32f_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32D</h2>')
    print('Analyzing RV32D instructions')    
    fo.write(_create_rv32d_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32A</h2>')
    print('Analyzing RV32A instructions')    
    fo.write(_create_rv32a_table(ins))
    fo.write('</td></tr></table>')

    fo.write('<table><tr><td valign="top">')
    fo.write('<h2>RV64I</h2>')
    print('Analyzing RV64I instructions')    
    fo.write(_create_rv64i_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV64M</h2>')
    print('Analyzing RV64I instructions')    
    fo.write(_create_rv64m_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV64F</h2>')
    print('Analyzing RV64F instructions')    
    fo.write(_create_rv64f_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV64A</h2>')
    print('Analyzing RV64A instructions')    
    fo.write(_create_rv64a_table(ins))
    fo.write('</td></tr></table>')

    fo.write('<table><tr><td valign="top">')
    fo.write('<h2>RVC</h2>')
    print('Analyzing RVC instructions')    
    fo.write(_create_rvc_table(ins))
    fo.write('</td></tr></table>')


    fo.write('<h2>Instructions</h2>')
    fo.write('<p>')
    for x in ins_set:
        fo.write('{} '.format( x))
    fo.write('</p>')
    
    fo.write('<h2>Registers</h2>')
    fo.write(_create_registers_table(regs))

    fo.write('<h2>ELF Section Information</h2>')
    fo.write(sectab)
    fo.write('</body>')
    fo.write('</html>')
    
def create_html_report_from_bin(binfile, htmlfile, elfclass):
    
    with open(binfile, 'rb') as fi:
        
        code = fi.read()
        code_len = len(code)
        
    print('Getting instructions')
    
    ins = riscv_ins.get_ins(code, elfclass)
    ins_set = set(ins)
    
    print('Getting register usage')
    regs = riscv_ins.get_regs(code, elfclass)
        
    fo = open(htmlfile, 'w')
    
    fo.write('<html>')
    fo.write('<body>')
    fo.write('<h1>RISC-V ISA Coverage Report for file {} </h1>'.format(binfile))
    fo.write('<p><small>This report is automatically created by <b>riscisacoverage</b> tool. Check <a href="https://github.com/davidcastells/riscvisacoverage">https://github.com/davidcastells/riscvisacoverage</a> </small></p><br>')
    fo.write('<table>')
    fo.write('<tr><td>File Path:</td><td>{}</td>'.format(binfile))
    fo.write('<tr><td>Report date:</td><td>{}</td>'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    fo.write('<tr><td>Elf class:</td><td>{}</td>'.format(elfclass))
    fo.write('<tr><td>Code Length:</td><td>{}</td>'.format(code_len))
    fo.write('</table>')

    fo.write('<table><tr><td valign="top">')
    fo.write('<h2>RV32I</h2>')
    print('Analyzing RV32I instructions')    
    fo.write(_create_rv32i_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32M</h2>')
    print('Analyzing RV32M instructions')    
    fo.write(_create_rv32m_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32F</h2>')
    print('Analyzing RV32F instructions')    
    fo.write(_create_rv32f_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32D</h2>')
    print('Analyzing RV32D instructions')    
    fo.write(_create_rv32d_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV32A</h2>')
    print('Analyzing RV32A instructions')    
    fo.write(_create_rv32a_table(ins))
    fo.write('</td></tr></table>')

    fo.write('<table><tr><td valign="top">')
    fo.write('<h2>RV64I</h2>')
    print('Analyzing RV64I instructions')    
    fo.write(_create_rv64i_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV64M</h2>')
    print('Analyzing RV64I instructions')    
    fo.write(_create_rv64m_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV64F</h2>')
    print('Analyzing RV64F instructions')    
    fo.write(_create_rv64f_table(ins))
    fo.write('</td><td valign="top">')
    fo.write('<h2>RV64A</h2>')
    print('Analyzing RV64A instructions')    
    fo.write(_create_rv64a_table(ins))
    fo.write('</td></tr></table>')

    fo.write('<table><tr><td valign="top">')
    fo.write('<h2>RVC</h2>')
    print('Analyzing RVC instructions')    
    fo.write(_create_rvc_table(ins))
    fo.write('</td></tr></table>')


    fo.write('<h2>Instructions</h2>')
    fo.write('<p>')
    for x in ins_set:
        fo.write('{} '.format( x))
    fo.write('</p>')
    
    fo.write('<h2>Registers</h2>')
    fo.write(_create_registers_table(regs))

    fo.write('</body>')
    fo.write('</html>')
    
def create_verilog(elffilename, verilogfile):
    
    print('ELFFile:', elffilename)
    with open(elffilename, 'rb') as fi:
        elffile = ELFFile(fi)
        
        text_section = elffile.get_section_by_name(".text")
        code = text_section.data()
        code_len = len(code)
        
    #print('Diassembly')
    
    ins = riscv_ins.get_ins(code)
    ins_set = set(ins)
    regs = riscv_ins.get_regs(code)
        
    fo = open(verilogfile, 'w')
    
    fo.write('// RISC-V ISA Coverage for file {}\n'.format(elffilename))
    fo.write('// This report is automatically created by riscisacoverage tool\n')
    fo.write('// Check https://github.com/davidcastells/riscvisacoverage\n')

    fo.write('// Instructions\n')
    for x in ins_set:
        fo.write('`define HAS_RISCV_INS_{} \n'.format(x))

    fo.write('// Registers\n')
    for x in regs:
        fo.write('`define HAS_RISCV_REG_{} \n'.format(x))
    
    fo.close()
    
def help():
    print('isariscvoerage [options]')
    print('')
    
    print('-i,--input <file>\tInput elf file')
    print('-w,--html <file>\tOutput html report file')
    print('-v,--verilog <file>\tOutput Verilog definition file')
    print('-h,--help\t\tshows this message')
    
if __name__ == "__main__":
    import sys
    
    if ('-h' in sys.argv)  or ('--help' in sys.argv) or (len(sys.argv) == 1):
        help()
        quit()
    
    input_file = None
    output_html = None
    output_verilog = None
    
    #print(sys.argv)
    i = 1
    max = len(sys.argv)
    while (i<max):
        arg = sys.argv[i]
        
        if ((i+1) < len(sys.argv)):
            next_arg = sys.argv[i+1]
        else:
            next_arg = None    
        
        if (arg == '-i') or (arg == '--input'):
            i += 1
            input_file = next_arg
        if (arg == '-w') or (arg == '--html'):
            i += 1
            output_html = next_arg
        if (arg == '-v') or (arg == '--verilog'):
            i += 1
            output_verilog = next_arg
            
        i += 1
    
        
    if (input_file is None):
        print('Error! No input file provided!')
        quit(-1)
        
    if not(output_html is None):
        create_html_report(input_file, output_html)
        
    if not(output_verilog is None):
        create_verilog(input_file, output_verilog)