all: adpcm.riscv32.elf adpcm.x86.elf

adpcm.riscv32.elf: adpcm_main.cpp
	riscv32-unknown-elf-g++ adpcm_main.cpp -O3 -flto -o adpcm.riscv32.elf


adpcm.x86.elf: adpcm_main.cpp
	g++ adpcm_main.cpp -O3 -flto -o adpcm.x86.elf

clean:
	rm -fr *.elf
