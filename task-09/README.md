## Operation Kernel

### Fixing Syntax errors
I quickly fixed some syntax errors. Here are they:
- lines 128, 134, 164 in interrupts (and all the constants of amfoss to upper case)
- line 78 of vga_buffers
- line 15 of gdt.rs
- lines 21, 40-52 (commented out) in main.rs

### Fixing input
To reverse the input order, I commented out line 112 of interrupts.rs

### Changing the theme
To change the background color and text color, I interchanged the color codes of black and red.
I found out that the keyboard input address was already correct (0x60).
