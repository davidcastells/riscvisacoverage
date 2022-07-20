# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 07:33:31 2022

@author: dcr
"""

import sys

sys.path.append('..')

import riscisacoverage as isacov

isacov.create_html_report('CHStone/adpcm/adpcm_main.riscv32.elf', 'adpcm.riscv32.elf.html')
isacov.create_html_report('CHStone/aes/aes_main.riscv32.elf', 'aes.riscv32.elf.html')
isacov.create_html_report('CHStone/blowfish/blowfish_main.riscv32.elf', 'blowfish.riscv32.elf.html')
isacov.create_html_report('CHStone/dfadd/float64_add.riscv32.elf', 'float64_add.riscv32.elf.html')

print('done!')
