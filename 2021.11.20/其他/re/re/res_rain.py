import re 

def plus(matched):
	value = int(matched.group('volume'))
	if value + 100 < 128:
		return 'v' + str(value + 100)
	else:
		return 'v' + str(value)


input_file = 'test.gwi'
output_file = 'output.gwi'

with open(input_file, 'r', encoding='utf8') as f:
	data = f.read()


# s = 'F1 T125 @1 v25 o6 d+12&d+32r96o6 g+12&g+32r96 v44 a+12&a+32r96 v50 a+8..r64r96>c8..r64r96'

output_data = re.sub('v(?P<volume>[0-9][0-9])', plus, data)

with open(output_file, 'w', encoding='utf8') as f:
	f.write(output_data)