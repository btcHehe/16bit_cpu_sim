# Simulator of 16-bit CPU

Gui simulator for imaginary 16-bit CPU. 

## Register list
All registers are 16-bit registers which are made of 8-bit registers. So every register has it's low and high part (nibble) which are accessed by using L or H letter (AX = AH and AL).
- AX
- BX
- CX
- DX

## CPU Features
- Stack
- Carry flag
- Zero flag
- Stack pointer
- Instruction pointer

## Assembly
### Instruction set
| Instruction       | Argument 1        | Argument 2    | Description           |
| -------------     |:----------------: | ------------: | --------------------: |
| ADD               | REG 1, NUMBER     |    REG 2      | Add argument 1 to argument 2. Save result in argument 2                 |
| SUB               | REG 1, NUMBER     |    REG 2      | Subtract argument 1 from argument 2. Save result in argument 2 |
| MOV               | REG 1, NUMBER     |    REG 2      | Copy given value or value of given register in argument 1 to register in argument 2 |
| PUSH              | REG               |    -          | Save value of given register on top of the stack |
| POP               | REG               |    -          | Pop value from to of the stack and save it in given register |
| JMP               | LABEL             |    -          | Unconditional jump to given label |
| JZ                | LABEL             |    -          | Jump when zero flag is set. Jump to line described with label |
| JC                | LABEL             |    -          | Jump when carry flag is set. Jump to line described with label |
| INC               | REG               |    -          | Increment given register by 1 |
| DEC               | REG               |    -          | Decrement given register by 1 |
| ORL               | REG 1             |    REG 2      | Logical or between given registers. Result saved in argument 2 |
| ANDL              | REG 1             |    REG 2      | Logical and between given registers. Result saved in argument 2 |
| XORL              | REG 1             |    REG 2      | Logical xor between given registers. Result saved in argument 2 |
| CRL               | REG               |    -          | Clear given register (set its value to 0) |
| ROR               | REG               |    -          | Rotate given register right |
| ROL               | REG               |    -          | Rotate given register left |
| SHR               | REG               |    -          | Shift right given register by one bit |
| SHL               | REG               |    -          | Shift left given register by one bit |


## Simulator GUI
![Gui screenshot](img/gui.png)