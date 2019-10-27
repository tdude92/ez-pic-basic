# quickpb
An easy and efficient language that compiles into PIC BASIC for the programming of a 4x4 LED cube using a PIC16f887a microcontroller. Made with @Keraisyn.

## Compilation Instructions
The python file *qpbcompile.py* compiles files with the .qpb extension into .picb files containing PIC BASIC code.

    python qpbcompile.py [-a|s file_name]
    
or

    python3 qpbcompile.py [-a|s file_name]
 
# Compiler Flags
**-a**: Compile all .qbp files in the same directory as qbpcompile.py
**-s file_name**: Only compile file_name (Don't forget to add the .qbp extension to the end of file_name).

## Language Guide
FIRST OF ALL, you'll have to make sure that the ports of the PIC16f887a are connected to the LED cube like this:
    
    Top View:
      B7 B6 B5 B4
      B3 B2 B1 B0
      D7 D6 D5 D4
      D3 D2 D1 D0
    
    Side View:
    C7
    C6
    C5
    C4
      D3 D2 D1 D0

You'll also have to get familiar with how each LED is named on a 4x4 LED cube. \
**quickpb** uses a sort of "coordinate system" to identify each LED. Essentially, each LED will have a three digit ID where the first digit is the x-value, the second is the y-value, and the third is the z-value (xyz). On each axis, there are four LEDs that are numbered from 0 to 3. IT should look something like this.

    Top View:
    ^ 3      B7 B6 B5 B4
    | 2      B3 B2 B1 B0
    | 1      D7 D6 D5 D4
    z 0      D3 D2 D1 D0
    
    Side View:
    ^ 3    C7
    | 2    C6
    | 1    C5
    y 0    C4
             D3 D2 D1 D0
             
             0  1  2  3
             x -------->

So as an example, the ID of the LED in the bottom right corner of the side view would be **300**.\

Alright, let's get started with some coding.\
The LED cube animation is split up into "frames". One frame represents the LED cube at a specific point in time; it describes which LEDs are lit and which remain unlit. A frame of an animation is described by a single line of space-separated LED IDs.

    000 100 200 300
    // The LEDs: 000, 100, 200, and 300 are lit in this frame.
    // By the way, you can comment with double forward-slashes (//).
    // There aren't any multiline comments, sry.
    001 101 201 301
    // The LEDs: 001, 101, 201, and 301 are lit in this frame.

Each frame is 40ms long, which is usually good enough for most situations, but what if you need a lower framerate? This can be resolved by looping frames (We'll get into loops soon).\
Unfortunately, this means that the length of a frame can only be a multiple of 40ms.\
On the bright side, we are also able to specify the brightness of a single LED by appending a "brightness" digit to the end of an LED ID.

    0000 1003 2006 3009
    // 000 has a brightness of 0
    // 100 has a brightness of 3
    // 200 has a brightness of 6
    // 300 has a brightness of 9
    
    // When there is no brightness digit, the compiler assumes that the LED have a brightness of 9.

The brightness digit can be between 0 and 9, where 0 is the lowest possible brightness where the LED remains while 9 is the highest possible brightness of an LED.\
\
The last thing you'll need to know to be able to use quckpicbasic is the looping tools that are available to you. There are only two commands that you need to know:
* LOOP <loopname> <number of iterations>
* GOTO <loopname>
    
As evident by their names, LOOP specifies the beginning of a loop, its name, and the number of iterations, while GOTO specifies the part that loops back to the beginning.

    LOOP mainloop 1000
    000 100 200 300 020 120 220 320
    201 202 203
    GOTO mainloop
    // This code loops over two frames 1000 times.

That's it, have fun passing Mr Webb's class.
