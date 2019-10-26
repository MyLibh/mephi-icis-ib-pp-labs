import gdb
import re

def words_in_line(words, line):
    return set(words).intersection(line.split())

class ProgViewer:
    mov = ['mov', 'movss', 'movsd']
    remove_list = ['', '=>']

    def __init__(self, file):
        self.vars = {}

        gdb.execute('file ' + file, to_string=True)

    def _rec_prog_locals(self, func, rec_level):
        if func == None or rec_level > 5:
            return

        gdb.execute('b ' + func, to_string=True)
        if rec_level == 0:
            gdb.execute('r ', to_string=True)
        else:
            gdb.execute('c', to_string=True)

        print('\t'*rec_level + 'FRAME<lvl={}> [{}]'.format(rec_level, func))
        disasm = gdb.execute('disassemble {}'.format(func), to_string=True).split('\n')
        for line in disasm:
            if 'call ' in line:
                func_name = line.split('call ')[1].strip().split(' ')[1]
                func_name = func_name[1:len(func_name)-1]
                if func_name != '__stack_chk_fail@plt':
                    self._rec_prog_locals(func_name, rec_level+1)
            elif 'fstp ' in line:
                print('I do not wanna parse({})'.format(line.strip()))
            elif words_in_line(ProgViewer.mov, line) and ('[' in line) and (']' in line):
                data = list(filter(lambda x: x != '' and x != '=>', line.strip().split(' ')))

                var_type = data[2]
                try:
                    stack_addr, var_value = data[4].split(',')
                    stack_addr = stack_addr[1:len(stack_addr)-1]
                except:
                    print('Cannot parse({})'.format(line.strip()))
                    continue
                
                c = 'b'
                if var_type == 'WORD':
                    c = 'h'
                elif var_type == 'DWORD':
                    c = 'w'
                elif var_type == 'QWORD':
                    c = 'g'

                var_addr = re.sub(r'\s+', r'', gdb.execute('x/{}x ${}'.format(c, stack_addr), to_string=True)).split(':')[0]                
                print('\t'*rec_level + '{:>14} {:>5} {:>15}'.format(var_addr, var_type, var_value))

    def prog_locals(self):
        self._rec_prog_locals('main', 0)

    def func_locals(self, func_name):
        gdb.execute('b ' + func_name, to_string=True)
        gdb.execute('r', to_string=True)
        disasm = gdb.execute('disassemble {}'.format(func_name), to_string=True).split('\n')
        for line in disasm:
            if 'fstp ' in line:
                print('I do not wanna parse({})'.format(line.strip()))
            elif words_in_line(ProgViewer.mov, line) and ('[' in line) and (']' in line):
                data = list(filter(lambda x: x != '' and x != '=>', line.strip().split(' ')))

                var_type = data[2]
                try:
                    stack_addr, var_value = data[4].split(',')
                    stack_addr = stack_addr[1:len(stack_addr)-1]
                except:
                    print('Cannot parse({})'.format(line.strip()))
                    continue
                    
                c = 'b'
                if var_type == 'WORD':
                    c = 'h'
                elif var_type == 'DWORD':
                    c = 'w'
                elif var_type == 'QWORD':
                    c = 'g'
                # elif var_type == 'TWORD':
                #     c = 't'

                var_addr, cur_val = re.sub(r'\s+', r'', gdb.execute('x/{}x ${}'.format(c, stack_addr), to_string=True)).split(':')                 
                self.vars[var_addr] = [var_type, var_value, cur_val]

    def reset(self):
        self.vars.clear()

    def print_nice_line(self):
        print('+=' + '='*14 + '=+=' + '='*5 + '=+=' + '='*15 + '=+=' + '='*18 + '=+')

    def print_vars(self):
        if len(self.vars) > 0:
            self.print_nice_line()
            print('| {:^14} | {:^5} | {:^15} | {:^18} |'.format('ADDRESS', 'TYPE', 'INITIAL_VALUE', 'CURRENT_VALUE'))
            self.print_nice_line()
            for var in self.vars:
                print('| {:>14} | {:>5} | {:>15} | {:>18} |'.format(var, self.vars[var][0], self.vars[var][1], self.vars[var][2]))
            self.print_nice_line()
        else:
            print('No variables detected')

def main():
    file = 'test'
    func = None

    pv = ProgViewer(file)
    if func != None:
        pv.func_locals(func)
        pv.print_vars()
    else:
        pv.prog_locals()

if __name__ == "__main__":
    main()