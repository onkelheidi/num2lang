#!/usr/local/bin/python3.5
import re

def get_digit ( num, digit ):
	w_o_right_part = int( num / 10**digit )
	return w_o_right_part % 10

def get_digit_count ( num ):
	digit_count = 0
	num_copy = num
	while num_copy != 0:
		num_copy = int( num_copy / 10 )
		digit_count += 1
	if 0 == digit_count:
		return 1
	return digit_count

def get_digit_count_left_from_digit ( num, digit ):
	digit_count = get_digit_count( num )
	return digit_count - digit - 1

def get_digit_count_right_from_digit ( num, digit ):
	return digit

def get_digit_regex ( num, digit ):
	regex = r''
	for i in range( 0, get_digit_count( num ) ):
		if i == digit:
			regex = r'\[' + str( get_digit( num, digit ) ) + r'\]' + regex
		else:
			regex = r'[x' + str( get_digit( num, i ) ) + r']' + regex
	regex += r':\s?(.*?)$'
	regex = r'^' + regex
	return regex

def get_digit_name ( language_base_data, num, digit ):
	
	#try to find regex hits
	new_num = num
	regex_match = None
	
	#if no regex has been found, remove one digit
	while True:
		#(emulate repeat..until)
		regex_object = re.compile( get_digit_regex( new_num, digit ), re.MULTILINE )
		regex_match = regex_object.search( language_base_data )
		if regex_match != None:
			#return name, exits loop
			return regex_match.group(1)
		else:
			#no match, try to find another name for that digit
			#only if there are digets before the requested digits to remove
			if 0 < get_digit_count_left_from_digit( new_num, digit ):
				#remove digit
				new_num = new_num % 10**( get_digit_count( new_num ) - 1 )
			else:
				#no name for this diget available at all, kill yourself
				raise LookupError('Can\'t find the name for the digit No. ' + str( digit ) + ' in the number ' + str( num ) + ' (this digit being ' + str( get_digit( num, digit ) ) + ')' )

def get_number_name ( language_base_data, num ):
	#try to find a map for this number length
	#generate regex for this map
	regex = r''
	for i in range( get_digit_count( num ) ):
		regex = r'([A-Z' + str( get_digit( num, i ) ) + r'])' + regex
	regex = r'^@' + regex
	regex = regex + r':\s?(.*?)$' #note: lazy, so the whitespace is not catched
	
	#try to find any matches
	regex_object = re.compile( regex, re.MULTILINE )
	regex_match = regex_object.search( language_base_data )
	if None == regex_match:
		#no rule saved: kill yourself
		raise LookupError('Can\'t find a suitable rule for the number ' + str( num ) )
	
	#get the last group, aka the actual string part of the rule, e.g .@AB: >%%A%%%%B%%<
	name = regex_match.group( get_digit_count( num ) + 1 )
	#get all digit codes, e.g. [A, B, C] in @ABC: %%A%%%%B%%
	all_digit_codes = []
	for i in range( get_digit_count( num ) ):
		all_digit_codes.append( regex_match.group( i + 1 ) )
	
	#find e.g. [AB]
	subparts_regex = r'\[([' + ''.join( all_digit_codes ) + r']+)\]'
	subparts_regex_object = re.compile( subparts_regex )
	for subparts_regex_match in subparts_regex_object.finditer( name ):
		#build new sub-number
		to_replace = subparts_regex_match.group(1)
		#replace single digits
		for i in range( 0, get_digit_count( num ) ):
			#check: is this digit name even requested:
			digit_code = regex_match.group( get_digit_count( num ) - i ) #the name for the digit, e.g. @>A<B: %%A%%%%B%%
			if digit_code in to_replace:
				#get content for this digit (e.g. 1 or 3)
				digit_content = str( get_digit( num, i ) )
				to_replace = to_replace.replace( digit_code, digit_content )
		#generate name for the sub-number
		subnumber_name = get_number_name( language_base_data, int( to_replace ) ) #note: no check for valid integer as every digit has been replaced (due to wise selection with regex)
		subpart_replacement = subparts_regex_match.group() #the whole matched regex
		name = name.replace( subpart_replacement, subnumber_name )

	#replace e.g. %%A%%
	for i in range( 0, get_digit_count( num ) ):
		#check: is this digit name even requested:
		digit_code = regex_match.group( get_digit_count( num ) - i ) #the name for the digit, e.g. @>A<B: %%A%%%%B%%
		digit_replacement = '%%' + digit_code + '%%'
		if digit_replacement in name:
			#get name for this digit
			digit_name = get_digit_name( language_base_data, num, i )
			name = name.replace( digit_replacement, digit_name )
	return name

def get_number_length ( language_base_data ,num ):
	return len( get_number_name( language_base_data, num ) )

def get_numberchain ( language_base_data, num, appeared_numbers ):
	length = get_number_length( language_base_data, num )
	print( 'num: ' + str(num) )
	if length in appeared_numbers:
		return [ str( length ) ]
	else:
		appeared_numbers.append( length )
		array = get_numberchain( language_base_data, length, appeared_numbers )
		array.append( str( length ) )
		return array

def get_chain_length ( language_base_data, num ):
	chain = get_numberchain( language_base_data, num, [] )
	return len( chain ) - 1

def get_possible_numbers_by_rule ( rule ) :
	if len( rule ) == 1:
		regex_is_number = r'[0-9]'
		regex_is_number_object = re.compile( regex_is_number )
		regex_is_number_match = regex_is_number_object.search( rule )
		if regex_is_number_match != None:
			#match == is number
			return [ int( rule ) ]
		else:
			#no match == is not number == is placeholder for >any< digit
			return list( range( 10 ) )
	else:
		#rule length > 1
		all_possibilities = []
		first_char_posibilities = get_possible_numbers_by_rule( rule[0] )
		rest_rule = rule[1:] #everything after index 1 aka remove 1st char
		rest_rule_possibilities = get_possible_numbers_by_rule( rest_rule )
		#remove 1st char
		for single_possible_digit in first_char_posibilities:
			for single_possible_rest_number in rest_rule_possibilities:
				possible_number = ( single_possible_digit * ( 10**get_digit_count( single_possible_rest_number ) ) ) + single_possible_rest_number
				all_possibilities.append( possible_number )
		all_possibilities = list( set( all_possibilities ) ) #each value only once
		return all_possibilities

def get_possible_numbers ( language_base_data ):
	regex = r'^@([0-9A-Z]+):'
	regex_object = re.compile( regex, re.MULTILINE )
	#get all rules
	all_possibilities = []
	for single_regex_match in regex_object.finditer( language_base_data ):
		all_possibilities.extend( get_possible_numbers_by_rule( single_regex_match.group(1) ) )
	all_possibilities = list( set( all_possibilities ) ) #each value only once
	return all_possibilities


german_base_data = '''
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
'''

english_base_data = '''
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
'''

base_data = english_base_data

print( get_number_name( base_data, 1 ) )
print( get_number_name( base_data, 13 ) )
print( get_number_name( base_data, 11 ) )
print( get_number_name( base_data, 10 ) )
print( get_number_name( base_data, 20 ) )
print( get_number_name( base_data, 30 ) )
print( get_number_name( base_data, 40 ) )
print( get_number_name( base_data, 50 ) )
print( get_number_name( base_data, 100 ) )
print( get_number_name( base_data, 200 ) )
print( get_number_name( base_data, 300 ) )
print( get_number_name( base_data, 400 ) )
print( get_number_name( base_data, 345 ) )
print( get_number_name( base_data, 3452 ) )
print( get_number_name( base_data, 3455 ) )
print( get_number_name( base_data, 13455 ) )
print( get_number_name( german_base_data, 99999 ) )

print('eng.')
chain = get_numberchain( english_base_data, 1337, [] )
chain.reverse()
print( ' => '.join( chain ) )
print('ger.')
chain = get_numberchain( german_base_data, 1337, [] )
chain.reverse()
print( ' => '.join( chain ) )

all_possible_german_numbers = get_possible_numbers( german_base_data )
print( min( all_possible_german_numbers ) )
print( max( all_possible_german_numbers ) )