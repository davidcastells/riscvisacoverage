all: aes_main.riscv32.elf

aes_main.riscv32.elf: aes_main.cpp
	riscv32-unknown-elf-g++ aes_main.cpp -o aes_main.riscv32.elf


aes_main.x86.elf: aes_main.cpp
	g++ aes_main.cpp -o aes_main.x86.elf
