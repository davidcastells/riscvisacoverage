# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 07:33:31 2022

@author: dcr
"""

import sys

sys.path.append('..')

import riscisacoverage as isacov

isacov.create_html_report('test.riscv-32.exe', '../docs/test.riscv-32.html')
isacov.create_html_report('test_nostd.riscv-32.exe', '../docs/test_nostd.riscv-32.html')

print('done!')
