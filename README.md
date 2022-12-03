# riscvisacoverage
Extract the RISC-V ISA instructions used by an application.

By now it supports the following ISA instructions:
RV32I, RV32M, RV32F, RV32D, RV32A, RV64I, RV64M, RV64F, RV64A, RVC

More coming soon!

check the examples 

[example1: a 32bit hello world application linked with C runtime](https://davidcastells.github.io/riscvisacoverage/test.riscv-32.html)

[example2: a 32bit hello world application not using C runtime, directly calling putchar ECALL](https://davidcastells.github.io/riscvisacoverage/test_nostd.riscv-32.html)

[example3: a 64bit linux kernel](http://davidcastells.github.io/riscvisacoverage/test_vmlinux.html)
