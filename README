# num2lang
Num2lang is a simple project to generate written numbers, e.g. "fifty-five" from integers, such as 55.

## Implementation
It is developed in the python programming language version 3.5, but is compatible with any python version above 3 (3.x).
Tested versions:

- Python 3.5, Ubuntu Linux
- Python 3.4, Ubuntu Linux

## Usage
Num2lang ships with various functions. To simply convert an integer into a language, use
```python
print( get_number_name( language_base_data, num ) )
```
`language_base_data` being the definition of a language, and `num` being the integer to convert.

## Language Definition
Languages are defined using a custom definition language.
There are two basic concepts to this language:

- defining single digits
- defining how to put single digits together

### Assumptions
#### Leading Zeros
Num2Lang ignores leading zeros. So if there is a rule how to convert 123456, 12345 will not be affected by this rule.
This way you can be sure, the first digit is never a zero.
#### General Syntax
Each rule has to be on its own line. Leading spaces render a rule invalid.
After the colon `:` there can be one, but only one optional whitespace. Additional whitespaces are treated like being a part of the text.

#### Rule Priority
The first matching rule for a number is applied.
If the language Definition would be:
```
@AB: %%A%%%%B%%
@11: eleven
```
For the number 11 the rule in line No. 1 would match, even if the rule in line No. 2 would make more sense.

### Defining Single Digits
Examples:
```
[0]: nought
[1]: one
[2]: two
[3]: three
[4]: four
[5]: five
[6]: six
[7]: seven
[8]: eight
[9]: nine
[1]x: ten
[2]x: twenty
[3]x: thirty
[4]x: fourty
[5]x: fifty
[6]x: sixty
[7]x: seventy
[8]x: eighty
[9]x: ninety
```
The part before the colon `:` defines the structure of the number. You can place an `x` for any digit or use specific digits.
To make 65 be pronounced `sixty-fiiive`, but 5 as `five` and 45 as `fourty-five`, the definition got to be:
```
[5]: five
[4]x: fourty
[5]x: fifty
6[5]: fiiive
```
This defines only single digits. To define how to put these digit names together, we have to look at the next section.

### Defining Full Numbers
If you have defined the single digits, you can define how to put these digits together.
The Rules for english up to 5 digits are:
```
@Z: %%Z%%
@11: eleven
@12: twelve
@13: thirteen
@15: fifteen
@Y: %%Y%%
@YZ: %%Y%%%%Z%%
@X: [X]hundred
@X0Z: [X]hundred and [Z]
@XYZ: [X]hundred[YZ]
@WXYZ: [W]thousand[XYZ]
@VWXYZ: [VW]thousand[XYZ]
```
Each rule begins with an `@` and uses either __upper-case__ letters or numbers to define the general structure of the number to convert.
Three kind of structure can be used:

1. Literal Text
	any text written after the colon is transfered to the final number
1. Digit Lookups
	Any `%%<upper-case character>%%` is replaced with the name of that digit
1. Number Mixins
	Any `[ABC]` within the string is replaced with the full name of that number

#### What's the difference between %%A%% and [AB]
The place where to name is looked up.
While `%%A%%` tries to find a name for that digit, `[AB]` doesn't do that and tries instead to convert the number `AB` (with replaced digits).
`%%A%%` looks up in this block:
```
...
[8]: eight
[9]: nine
[1]x: ten
[2]x: twenty
[3]x: thirty
...
```
`[AB]` looks up in this block
```
...
@13: thirteen
@15: fifteen
@Y: %%Y%%
@YZ: %%Y%%%%Z%%
@X: [X]hundred
@X0Z: [X]hundred and [Z]
@XYZ: [X]hundred[YZ]
...
```

## Example Languages

### English up to 5 digits
```
@Z: %%Z%%
@11: eleven
@12: twelve
@13: thirteen
@15: fifteen
@Y: %%Y%%
@YZ: %%Y%%%%Z%%
@X: [X]hundred
@X0Z: [X]hundred and [Z]
@XYZ: [X]hundred[YZ]
@WXYZ: [W]thousand[XYZ]
@VWXYZ: [VW]thousand[XYZ]
[0]: nought
[1]: one
[2]: two
[3]: three
[4]: four
[5]: five
[6]: six
[7]: seven
[8]: eight
[9]: nine
[1]x: ten
[2]x: twenty
[3]x: thirty
[4]x: fourty
[5]x: fifty
[6]x: sixty
[7]x: seventy
[8]x: eighty
[9]x: ninety
```

### German up to 5 digits
```
@A: %%A%%
@11: elf
@12: zwölf
@16: sechzehn
@A0: %%A%%
@1A: %%A%%zehn
@AB: %%B%%und%%A%%
@C00: %%C%%
@C0B: %%C%%und%%B%%
@CAB: %%C%%[AB]
@1BCD: eintausend[BCD]
@ABCD: [A]tausend[BCD]
@ABCDE: [AB]tausend[CDE]
[0]: null
[1]: eins
[2]: zwei
[3]: drei
[4]: vier
[5]: fünf
[6]: sechs
[7]: sieben
[8]: acht
[9]: neun
[1]x: zehn
[2]x: zwanzig
[3]x: dreißig
[4]x: vierzig
[5]x: fünfzig
[6]x: sechzig
[7]x: siebzig
[8]x: achtzig
[9]x: neunzig
[1]xx: hundert
[2]xx: zweihundert
[3]xx: dreihundert
[4]xx: vierhundert
[5]xx: fünfhundert
[6]xx: sechshundert
[7]xx: siebenhundert
[8]xx: achthundert
[9]xx: neunhundert
```