import re 

def plus(matched):
	global min_inc
	value = int(matched.group('volume'))
	return 'v' + str(value + min_inc)


input_file = 'test.gwi'
output_file = 'output.gwi'
p_str = 'v(?P<volume>[0-9][0-9])'
min_inc = 0

with open(input_file, 'r', encoding='utf8') as f:
	data = f.read()


# s = 'F1 T125 @1 v37 o6 d+12&d+32r96o6 g+12&g+32r96 v44 a+12&a+32r96 v50 a+8..r64r96>c8..r64r96 v37 c8&c96& c1&'

pattern = re.compile(p_str)
result = pattern.findall(data)
min_inc = 127 - max([int(x) for x in result])

output_data = re.sub(p_str, plus, data)

with open(output_file, 'w', encoding='utf8') as f:
	f.write(output_data)