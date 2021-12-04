import configparser
import os
import re


class mv2_conv:
    config_file = 'settings.ini'
    input_file_list = []
    tone_list = []
    channel_list = []
    p_str = 'v(?P<volume>[0-9]+)'
    o_str = 'o(?P<pitch>[0-9]+)'
    t_str = '@(?P<tone>[0-9]+)'
    c_str = "'[A-Z][s]?(?P<channel>[0-9]+)"
    conf = 0
    channel = 'F'
    tmax = 0
    tmin = 0
    vmax = 0
    vmin = 0
    mode = 0
    out_name = '-out'
    vrate = 0.1
    pitch_inc = 0


    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('settings.ini', encoding='utf-8')
        items = self.conf.items('m2v')
        for x, y in items:
            if x == 'tmax':
                self.tmax = int(y)
            elif x == 'tmin':
                self.tmin = int(y)
            elif x == 'mode':
                self.mode = int(y)
            elif x == 'vrate':
                self.vrate = float(y)
            elif x == 'outname':
                self.out_name = y
            elif x == 'channel':
                self.channel = y
        for x in os.listdir(os.getcwd()):
            if x.endswith('.gwi') and self.out_name not in x:
                self.input_file_list.append(x)
        if self.mode == 0:
            self.automode()
        else:
            self.mnmode()

    def normalize(self, value, max_val, min_val):
        return (value - min_val) / (max_val - min_val)

    def plus(self, matched):
        value = int(matched.group('volume'))
        return 'v' + str(round(self.normalize(value, self.vmax, self.vmin) * (self.tmax - self.tmin) + self.tmin))

    def add_pitch(self, matched):
        value = int(matched.group('pitch'))
        return 'o' + str(value + self.pitch_inc)

    def modi_tone(self, matched):
        value = int(matched.group('tone'))
        return '@' + str(self.tone_list.pop(0))

    def modi_channel(self, matched):
        value = int(matched.group('channel'))
        return '\'' + self.channel + str(self.channel_list.pop(0))

    def ajust_volume(self):
        for input_file in self.input_file_list:
            with open(input_file, 'r', encoding='utf8') as f:
                data = f.read()
            pattern = re.compile(self.p_str)
            result = pattern.findall(data)
            self.vmax = max([int(x) for x in result])
            self.vmin = min([int(x) for x in result])
            output_data = re.sub(self.p_str, self.plus, data)
            output_file = input_file[:-4] + self.out_name + '.gwi'
            with open(output_file, 'w', encoding='utf8') as f:
                f.write(output_data)
            print('Output to ' + output_file)

    def ajust_pitch(self):
        self.pitch_inc = int(input('Input pitch increment:'))
        for input_file in self.input_file_list:
            with open(input_file, 'r', encoding='utf8') as f:
                data = f.read()
            output_data = re.sub(self.o_str, self.add_pitch, data)
            output_file = input_file[:-4] + self.out_name + '.gwi'
            with open(output_file, 'w', encoding='utf8') as f:
                f.write(output_data)
            print('Output to ' + output_file)

    def ajust_tone(self):
        for input_file in self.input_file_list:
            with open(input_file, 'r', encoding='utf8') as f:
                data = f.read()
            pattern = re.compile(self.t_str)
            result = pattern.findall(data)
            self.tone_list = [i for i in result]
            print('All tones:')
            for i, val in enumerate(result):
                print(str(i + 1) + '. ' + val)
            index = int(input('Input index(0 to exit):'))
            while index != 0:
                new_tone = input('Input new tone(integer)')
                self.tone_list[index - 1] = int(new_tone)
                index = int(input('Input index(0 to exit):'))

            output_data = re.sub(self.t_str, self.modi_tone, data)
            output_file = input_file[:-4] + self.out_name + '.gwi'
            with open(output_file, 'w', encoding='utf8') as f:
                f.write(output_data)
            print('Output to ' + output_file)

    def ajust_channel(self):
        for input_file in self.input_file_list:
            with open(input_file, 'r', encoding='utf8') as f:
                data = f.read()
            pattern = re.compile(self.c_str)
            result = pattern.findall(data)
            self.channel_list = [i for i in result]
            print('All channels:')
            for i, val in enumerate(result):
                print(str(i + 1) + '. ' + val)
            index = int(input('Input channel(0 to exit):'))
            while index != 0:
                new_channel = input('Input new channel(integer)')
                self.tone_list[index - 1] = int(new_channel)
                index = int(input('Input index(0 to exit):'))

            output_data = re.sub(self.c_str, self.modi_channel, data)
            output_file = input_file[:-4] + self.out_name + '.gwi'
            with open(output_file, 'w', encoding='utf8') as f:
                f.write(output_data)
            print('Output to ' + output_file)

    def automode(self):
        self.ajust_volume()

    def mnmode(self):
        print('1. Adjust volume')
        print('2. Adjust pitch')
        print('3. Adjust tone')
        print('4. Adjust channel')
        option = int(input('Input your chioce:'))
        if option == 1:
            self.ajust_volume()
        elif option == 2:
            self.ajust_pitch()
        elif option == 3:
            self.ajust_tone()
        elif option == 4:
            self.ajust_channel()


if __name__ == '__main__':
    m = mv2_conv()
