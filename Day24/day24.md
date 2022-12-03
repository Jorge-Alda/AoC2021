# Dissecting the instructions

We can split the instructions in 14 blocks of 18 instructions each, which read and process each input digit:

## Blocks

### Block 00

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
```

### Block 01

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
```

### Block 02

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
```

### Block 03

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
```

### Block 04

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
```

### Block 05

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
```

### Block 06

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
```

### Block 07

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x -8
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
```

### Block 08

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
```

### Block 09

```text
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
```

### Block 10

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
```

### Block 11

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x -5
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
```

### Block 12

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
```

### Block 13

```text
inp w
mul x 0
add x z
mod x 26
div z 26
add x -12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
```

## Parsing the blocks

The basic structure of all blocks is

```text
01|  inp w
02|  mul x 0
03|  add x z
04|  mod x 26
05|  div z D
06|  add x A
07|  eql x w
08|  eql x 0
09|  mul y 0
10|  add y 25
11|  mul y x
12|  add y 1
13|  mul z y
14|  mul y 0
15|  add y w
16|  add y B
17|  mul y x
18|  add z y
```

The variable `w` is only ever used to store the last input value, and `x` and `y` are set to `0` before they are used. So at each block, we only have to keep track of the value stored in `z`. Each block only depends on three parameters: `A` and `B`, which are arbitrary integers, and `D`, which can only take the values `1` or `26`. Therefore, we can parse each block as a Python function:

```python
def block(z: int, w:int, A: int, B: int, D: bool) -> int
```

where `D` will be `True` if equal to `26`, and `False` if equal to `1`. We will see that `z` represents a "word" with characters in base-26, so we will instead define `z` as a `list` of `int`s, that we will modify in-place:

```python
def block(z: list[int], w:int, A: int, B: int, D: bool)
```

* The first line is simple enough, it reads a new value from the memory into `w`.
* Lines 2-4 clear the value of `x`, and store in it `z%26`, so now `x` contains the last character of `z`.

```python
def block(z: list[int], w: int, A: int, B: int, D: bool):
    if z == []:
        x = 0
    else:
        x = z[-1]
```

* In line 5, we calculate a quotient of `z`. If `D` is equal to `1` (`False` in our parsed version), the value of `z` is unchanged, and if `D` is equal to `26` (`True`), we are removing the last base-26 character. The last element is removed in blocks 03, 07, 08, 10, 11, 12 and 13.

```python
def block(z: list[int], w: int, A: int, B: int, D: bool):
    if z == []:
        x = 0
    else:
        x = z[-1]
    if D:
        z.pop()
```

* Lines 6-8 represent another conditional branching of the program. We compare the value stored in `w` (read from the memory) to `x+A`. `w` is guaranteed to be in the range 1-9, while `x` is in the range 0-25. So, for values of `A>9`, we will never enter in the conditional.

|Block|`A`|Conditional|
|-----|---|-----------|
|00   |11 |No         |
|01   |14 |No         |
|02   |10 |No         |
|03   |0  |Yes        |
|04   |12 |No         |
|05   |12 |No         |
|06   |12 |No         |
|07   |-8 |Yes        |
|08   |-9 |Yes        |
|09   |11 |No         |
|10   |0  |Yes        |
|11   |-5 |Yes        |
|12   |-6 |Yes        |
|13   |-12|Yes        |

Interestingly, the `Yes` occur in the blocks with `D` equal to 26.

```python
def block(z: list[int], w: int, A: int, B: int, D: bool):
    if z == []:
        x = 0
    else:
        x = z[-1]
    if D:
        z.pop()
    x = (x+A != w)
```

* Lines 9-12 store in `y` the value `26` if `x+A != w`, and `1` if `x+A == w`.
* In line 13, we multiply `z` by the value of `y`: if `x+A != w` we are "allocating" space for one new character at the end of the word, and if `x+A == w`, we are doing nothing.

```python
def block(z: list[int], w: int, A: int, B: int, D: bool):
    if z == []:
        x = 0
    else:
        x = z[-1]
    if D:
        z.pop()
    if x+A != w:
        z.append(...)
```

* In lines 14-16, we store `w+B` in the variable `y`.
* In line 15, we multiply `y` by the value of `x`, so it's different from zero only if `x+A != w`.
* And finally in line 16, we add `y` to `z`. If `x+A != 0`, we append `y=w+B` in the space we allocated in line 13. If `x+A == 0`, we do nothing:

```python
def block(z: list[int], w: int, A: int, B: int, D: bool):
    if z == []:
        x = 0
    else:
        x = z[-1]
    if D:
        z.pop()
    if x+A != w:
        z.append(w+B)
```

## Finding the solution

Now that we have translated the ALU-code into a more compact and readable Python function, we can work towards finding a solution. We are asked for memories which lead to a final value of `z = 0`, that in our Pythonized version means `z = []`.

In blocks 00, 01, 02, 04, 05, 06 and 09 we are forced to append new values to `z` (`len(z) += 7`), and we pop values in blocks 03, 07, 08, 10, 11, 12 and 13 (`len(z) -= 7`). So we must make sure that we must select the values of `w` such that `x+A == w` in blocks 03, 07, 08, 10, 11, 12 and 13.

|Block|`A`|`B`|`D`|`z`|Values|
|-----|---|---|---|---|---------|
|00   |11 |8  |`False`|`[w00+8]` |
|01   |14 |13 |`False`|`[w00+8, w01+13]` |
|02   |10 |2  |`False`|`[w00+8, w01+13, w02+2]`|
|03   |0  |7  |`True` |`[w00+8, w01+13]`|`w03=w02+2`
|04   |12 |11 |`False`|`[w00+8, w01+13, w04+11]`
|05   |12 |4  |`False`|`[w00+8, w01+13, w04+11, w05+12]`
|06   |12 |13 |`False`|`[w00+8, w01+13, w04+11, w05+4, w06+13]`
|07   |-8 |13 |`True` |`[w00+8, w01+13, w04+11, w05+4]`|`w07=w06+5`|
|08   |-9 |10 |`True` |`[w00+8, w01+13, w04+11]`|`w08=w05-5`|
|09   |11 |1  |`False`|`[w00+8, w01+13, w04+11, w09+1]`
|10   |0  |2  |`True` |`[w00+8, w01+13, w04+11]`|`w10=w09+1`
|11   |-5 |14 |`True` |`[w00+8, w01+13]`|`w11=w04+6`|
|12   |-6 |6  |`True` |`[w00+8]`|`w12=w01+7`|
|13   |-12|14 |`True` |`[]`|`w13=w00-4`

We can choose the values of `w00`, `w01`, `w02`, `w04`, `w05`, `w06` and `w09`, which will determine `w03`, `w07`, `w08`, `w10`, `w11`, `w12` and `w13`. We have to make sure that every value is in the range 1-9, and that we get the larger number, when read starting from `w00`:

|`w00`|`w01`|`w02`|`w03`|`w04`|`w05`|`w06`|`w07`|`w08`|`w09`|`w10`|`w11`|`w12`|`w13`|
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
|9 |2 |7 |9 |3 |9 |4 |9 |4 |8 |9 |9 |9 |5|

And now, in **Part 2** we are asked for the smallest number:

|`w00`|`w01`|`w02`|`w03`|`w04`|`w05`|`w06`|`w07`|`w08`|`w09`|`w10`|`w11`|`w12`|`w13`|
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
|5 |1 |1 |3 |1 |6 |1 |6 |1 |1 |2 |7 |8 |1 |
