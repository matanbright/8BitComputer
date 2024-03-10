# 8-Bit Computer

## Introduction

This is a simple programmable 8-bit computer that is built from scratch.

It's inspired by Ben Eater's 8-bit computer project: https://eater.net/8bit.

## How Does It Work?

The main component of the computer is the clock. It's the "heart" of the computer. The clock outputs a periodic signal to all the components in the computer at once. Every time this signal goes high, the various components in the computer commit an operation synchronously.

The "backbone" of the computer is the main bus. It is used to transfer data between the various components.

The next important component in the computer is the control unit. It controls the various components of the computer. It does that using control signals which are outputted through control lines that are spread across the computer and are connected to the various components. If for example, we want to transfer data between two registers, the control unit will have to output two signals before the clock signal goes high, one for enabling the output of the first register, and the other for enabling the input of the second register. When the clock signal goes high, the transfer operation will be committed. A simple operation like this is called a micro-instruction and it is defined in a micro-code (a pattern of control signals which are needed for performing a micro-instruction). An instruction consists of multiple micro-codes. When an instruction is executed, The control unit must perform the micro-codes of that instruction one after the other in order to complete the instruction. In order for the control unit to know which instruction to execute, the instruction needs to be loaded into the instruction register. The instruction register stores the code and parameter of the current instruction that is being executed. Please note that there are 2 general micro-codes that are executed before starting every instruction. They are responsible for loading the instruction from RAM to the instruction register, so the control unit will be able to execute the specific micro-codes for that instruction afterward.

In order for the computer to execute instructions, we will need to program it by writing the instructions to the RAM (Random Access Memory). In this computer we write to the RAM using physical switches on the board, that select the address in the RAM to write to, and the data to write). After the program is loaded to the RAM and we start the clock, the computer begins executing the instructions. In addition to the program's code, the RAM can also store data for use by the program, and it can also store variables that are saved in run-time by the program. The RAM address at which the current read/write operation is performed is stored in the memory address register.

To control the flow of the program and keep track of the current RAM address from which an instruction will be executed, there is the program counter. It's a counter (a special register that has an option to increment its value by one) that stores the RAM address at which the current instruction is located. Normally, when executing an instruction, the program counter is incremented so that the next instruction will be executed afterward, but if we change its value manually we can change the flow of the program.

The computer has 2 general-purpose registers, called A and B. These registers allow the saving of a single temporary 8-bit value, each one, that will be used by some operations.

In order for the computer to be able to perform arithmetic operations (like adding 2 numbers) it has an ALU (Arithmetic Logic Unit). This unit performs arithmetic operations by taking the values from registers A and B, and calculating them (using logic gates). This computer's ALU can only perform addition and subtraction. If we need to calculate the sum of two numbers, we will need to store the first number in register A, store the second number in register B, and output the data from the ALU. By doing that we will get the sum of these two numbers. There is also a control signal which causes the ALU to perform subtraction instead, so if we want to subtract the number stored in register B from the number stored in register A, the control unit must output the subtraction signal to the ALU before we read from the ALU.

The output of the computer is a 7-segment display. The displayed digits are changed according to the content of the output register. The display is controlled by a display-control unit which acts very similar to the control unit of the computer. There are signals which are outputted through control lines that each one is connected to a LED in a segment of a digit in the display. According to the value stored in the output register, the display-control unit outputs the appropriate signals which are required in order to display the digits of the number stored in the register (Please note that although this display has 4 different digits, the display-control unit only has outputs for a single 7-segment digit. So for displaying multi digits numbers, we need to use a technique that involves displaying only one digit at a time but doing it so quickly that the human eye can't tell. This is done using a dedicated timer).

## Components

The computer consists of the following components:

* **Clock** - Provides the clock signal that drives the computer and synchronizes all the operations.

* **Data Bus** - Allows data to be transferred between the various components.

* **Control Unit** - Controls all the components using a decoder that translates micro-codes to control signals.

* **Instruction Register** - Stores the code and parameter of the instruction that is being executed by the control unit.

* **RAM (Random Access Memory)** - Stores the program's code and data, and also temporary 8-bit values.

* **Memory Address Register** - Stores the current address that the RAM's read/write operations are performed at.

* **Program Counter** - Stores the RAM address of the current instruction that is being executed.

* **Registers A and B** - Store a temporary 8-bit value, each one, for use by some operations.

* **ALU (Arithmetic Logic Unit)** - Performs addition and subtraction on values from the A and B registers.

* **Display-Control Unit** - Controls the 7-segment display, using a decoder that translates numbers to display-control signals.

* **Output Register** - Stores the 8-bit value that is being displayed on the 7-segment display by the display-control unit.

## Control Signals

The control unit (which is found in the instruction register module) controls the behavior of the various components in the computer using signals. It sends them according to the current micro-code of the current instruction, using an instruction decoder in which all the micro-code definitions are flashed.

The available signals and their purpose are listed below:

| Signal Name | Description                                                                                |
|-------------|--------------------------------------------------------------------------------------------|
| PCin        | Connects the program counter's input lines to the bus                                      |
| PCout*      | Connects the program counter's output lines to the bus                                     |
| PCincrement | Sets the program counter to increment its value by one on the next high clock signal       |
| MARin       | Connects the memory address register's input lines to the bus                              |
| RAMin       | Connects the RAM's input lines to the bus                                                  |
| RAMout*     | Connects the RAM's output lines to the bus                                                 |
| IRin        | Connects the instruction register's input lines to the bus                                 |
| IRout*      | Connects the instruction register's output lines to the bus                                |
| RAin        | Connects the register A's input lines to the bus                                           |
| RAout*      | Connects the register A's output lines to the bus                                          |
| RBin        | Connects the register B's input lines to the bus                                           |
| ALUout*     | Connects the ALU's output lines to the bus                                                 |
| ALUsubtract | Causes the ALU to output a subtraction result instead of an addition result                |
| ORin        | Connects the output register's input lines to the bus                                      |
| RCreset     | Sets the micro-codes ring counter to reset its value to zero on the next high clock signal |
| Cstop       | Stops the clock of the computer                                                            |

_\* Only one signal from these can be outputted at a time because there can be only one component that outputs its data to the bus at a time. If multiple components are outputting their data to the bus at the same time, a short-circuit may occur which may cause the computer to restart, and in the worst case, it may even damage the components._

All the components that can transfer and receive data are connected to a shared 8-bit data bus (the main data bus of the computer). The control unit controls at any point in time which one component is writing to the bus, which components are reading from the bus, and which components are internally disconnected from the bus.
For example, if the control unit applies voltage on the "RAout" and "RBin" signals (while not applying voltage on the rest of the signals), it will cause register A to connect its output lines to the bus, register B to connect its input lines to the bus, and the rest of the components to be internally disconnected from the bus (and thus ignoring the data on it). When the clock signal goes high, the data from the outputting register (in this case, register A) will be transferred and stored in the inputting registers (in this case, register B only).

## Instructions

An instruction consists of 8 bits, of which the first 4 bits are the instruction parameter and the last 4 bits are the instruction code.\
Note: if an instruction doesn't have a parameter, the first 4 bits of the instruction are meaningless.

An instruction involves executing micro-codes, which are basic operations that the computer can do in a single clock cycle (like moving data between a register to another register), in order to complete itself.

The control unit has 2 EEPROM chips in which all the micro-codes are flashed.
The control signals are outputted from the EEPROMs depending on the current instruction (which is outputted from the instruction register) and on the current micro-code number (which is outputted from the micro-codes ring counter).\
Note: On the falling edge of the clock, the control unit changes the states of the control signals according to the current micro-code, and then, on the rising edge of the clock, all the operations are committed by the relevant components.

Before each instruction starts, there are 2 general micro-codes that are executed, regardless of the forthcoming instruction. Their purpose is to load the forthcoming instruction from the RAM, so the control unit will know what is the current instruction that needs to be executed. After each execution of these 2 general micro-codes, instruction-specific micro-codes are executed.

<pre>
<b>General micro-codes</b>:
  1) PCout, MARin                 :    Transfers the content of the program counter into the memory
                                       address register.
  2) RAMout, IRin, PCincrement    :    Transfers the content from the RAM at the address stored in the
                                       memory address register into the instruction register. At the same
                                       time, increments the program counter's stored value by one.
</pre>

---

Bellow are the instructions that the computer can perform:

<pre>
<b>NOP</b>
----------------------------------------
<b>Instruction Binary Code:</b> 0000
<b>Description:</b> Does nothing.

<b>Micro-codes</b>:
  3) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been incremented).
</pre>

<pre>
<b>LDA x</b>
----------------------------------------
<b>Instruction Binary Code:</b> 0001
<b>Description:</b> Loads the value from RAM at address 'x' into "A" register.

<b>Micro-codes</b>:
  3) IRout, MARin                 :    Transfers the content of the instruction register (only the 4 LSB
                                       bits, which are the instruction's parameter value) into the memory
                                       address register.
  4) RAMout, RAin                 :    Transfers the content from the RAM at the address stored in the
                                       memory address register into register A.
  5) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been incremented).
</pre>

<pre>
<b>STA x</b>
----------------------------------------
<b>Instruction Binary Code:</b> 0010
<b>Description:</b> Stores the value from "A" register in RAM at address 'x'.

<b>Micro-codes</b>:
  3) IRout, MARin                 :    Transfers the content of the instruction register (only the 4 LSB
                                       bits, which are the instruction's parameter value) into the memory
                                       address register.
  4) RAout, RAMin                 :    Transfers the content from register A into the RAM at the address
                                       stored in the memory address register.
  5) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been incremented).
</pre>

<pre>
<b>ADD x</b>
----------------------------------------
<b>Instruction Binary Code:</b> 0011
<b>Description:</b> Adds the value from RAM at address 'x' to "A" register.

<b>Micro-codes</b>:
  3) IRout, MARin                 :    Transfers the content of the instruction register (only the 4 LSB
                                       bits, which are the instruction's parameter value) into the memory
                                       address register.
  4) RAMout, RBin                 :    Transfers the content from the RAM at the address stored in the
                                       memory address register into register B.
  5) ALUout, RAin                 :    Transfers the value of the addition result from the ALU into
                                       register A.
  6) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been incremented).
</pre>

<pre>
<b>SUB x</b>
----------------------------------------
<b>Instruction Binary Code:</b> 0100
<b>Description:</b> Subtracts the value from RAM at address 'x' from "A" register.

<b>Micro-codes</b>:
  3) IRout, MARin                 :    Transfers the content of the instruction register (only the 4 LSB
                                       bits, which are the instruction's parameter value) into the memory
                                       address register.
  4) RAMout, RBin                 :    Transfers the content from the RAM at the address stored in the
                                       memory address register into register B.
  5) ALUsubtract, ALUout, RAin    :    Tells the ALU to perform subtraction and transfers the value of the
                                       subtraction result from the ALU into register A.
  6) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been incremented).
</pre>

<pre>
<b>JMP x</b>
----------------------------------------
<b>Instruction Binary Code:</b> 0101
<b>Description:</b> Jumps to address 'x' in RAM.

<b>Micro-codes</b>:
  3) IRout, PCin                  :    Transfers the content of the instruction register (only the 4 LSB
                                       bits, which are the instruction's parameter value) into the program
                                       counter.
  4) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been changed).
</pre>

<pre>
<b>OUT</b>
----------------------------------------
<b>Instruction Binary Code:</b> 1110
<b>Description:</b> Shows the value from "A" register on the digits display.

<b>Micro-codes</b>:
  3) RAout, ORin                  :    Transfers the content of register A into the output register.
  4) RCreset                      :    Resets the ring counter (it causes the 1st micro-code to be
                                       executed next, thus, ending the current instruction because the
                                       program counter's stored value has already been incremented).
</pre>

<pre>
<b>HLT</b>
----------------------------------------
<b>Instruction Binary Code:</b> 1111
<b>Description:</b> Stops the computer (stops the computer's clock).

<b>Micro-codes</b>:
  3) Cstop                        :    Stops the computer's clock (it causes the computer to freeze, thus,
                                       no further instructions will be executed. You will need to manually
                                       reset the computer to restart the clock).
</pre>

## Sample Programs

### Addition of Two Numbers

This program causes the computer to add the numbers 2 and 3, output the result, and then stop.

Assembly:
~~~assembly
            .code
[0x0]            LDA 0x4
[0x1]            ADD 0x5
[0x2]            OUT
[0x3]            HLT
            .data
[0x4]            0x2
[0x5]            0x3
~~~
Machine code:
~~~
[0x0]        00010100
[0x1]        00110101
[0x2]        11100000
[0x3]        11110000
[0x4]        00000010
[0x5]        00000011
~~~

### Counting

This program causes the computer to output consecutive numbers one by one (please note that values can only be between -128 and 127 because the maximum size of the output register is 8 bits).

Assembly:
~~~assembly
            .code
[0x0]            ADD 0x3
[0x1]            OUT
[0x2]            JMP 0x0
            .data
[0x3]            0x1
~~~
Machine code:
~~~
[0x0]        00110011
[0x1]        11100000
[0x2]        01010000
[0x3]        00000001
~~~

### The Fibonacci Sequence

This program causes the computer to output the numbers in the Fibonacci sequence one by one (please note that values will start to be invalid after 127 because the maximum size of the output register is 8 bits so an overflow will occur).

Assembly:
~~~assembly
            .code
[0x0]            LDA 0xC
[0x1]            STA 0xE
[0x2]            STA 0xF
[0x3]            LDA 0xD
[0x4]            OUT
[0x5]            STA 0xE
[0x6]            ADD 0xF
[0x7]            OUT
[0x8]            STA 0xF
[0x9]            ADD 0xE
[0xA]            OUT
[0xB]            JMP 0x5
            .data
[0xC]            0x0
[0xD]            0x1
~~~
Machine code:
~~~
[0x0]        00011100
[0x1]        00101110
[0x2]        00101111
[0x3]        00011101
[0x4]        11100000
[0x5]        00101110
[0x6]        00111111
[0x7]        11100000
[0x8]        00101111
[0x9]        00111110
[0xA]        11100000
[0xB]        01010101
[0xC]        00000000
[0xD]        00000001
~~~
