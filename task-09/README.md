## Operation Kernel

I quickly fixed some syntax errors. Here are they:
lines 128, 134, 164 in interrupts (and all the constants of amfoss to upper case)
line 78 of vga_buffers
line 15 of gdt.rs
lines 21, 40-52 (commented out) in main.rs
(Btw the commits in [link](https://github.com/BiscuitBobby/ruskos-problem-repo/commit/2ffa549b39d6f6a4cd8f889cbf56e211162078f2) show some of the undeleted syntax errors tho I found out later after fixing the syntax errors)
To reverse the input order, I commented out line 112 of interrupts.rs 
To change the background color and text color, I interchanged the color codes of black and red.
I found out that the keyboard input address was already correct (0x60).
