# quickpb
An easy and efficient language that compiles into PIC BASIC for the programming of a 4x4 LED cube using a PIC16f887a microcontroller. Made with @Keraisyn.

## Compilation Instructions
The python file *qbpcompile.py* compiles files with the .qbp extension into .picb files containing PIC BASIC code.

    qbpcompile.py [-a|s file_name]
 
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

So as an example, the ID of the LED in the bottom right corner of the side view would be **300**.

TO BE CONTINUED
