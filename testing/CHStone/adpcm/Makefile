all: adpcm_main.riscv32.elf

adpcm_main.riscv32.elf: adpcm_main.cpp
	riscv32-unknown-elf-g++ adpcm_main.cpp -O3 -flto -o adpcm_main.riscv32.elf


adpcm_main.x86.elf: adpcm_main.cpp
	g++ adpcm_main.cpp -O3 -flto -o adpcm.x86.elf
