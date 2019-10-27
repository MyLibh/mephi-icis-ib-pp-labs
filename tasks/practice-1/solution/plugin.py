import gdb
import re

# https://www.sourceware.org/gdb/onlinedocs/gdb/Commands-In-Python.html

class ProgViewer(gdb.Command):
    mov = ['mov', 'movss', 'movsd']
    types = ['BYTE', 'WORD', 'DWORD', 'QWORD', 'TWORD']

    def __init__(self):
        self.vars = {}

        super().__init__("locals", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        if arg == 'all': 
            return self.prog_locals()

        if arg == 'help':
            print('''Usage:\nlocals      - show locals from current frame.\nlocals all  - all locals variables.\nlocals func - all locals from func.''')
            return 0     
        elif len(arg) == 0 or arg == 'func':
            try:
                frame = gdb.selected_frame()
            except:
                print("Frame is invalid")
                return -1

            if len(arg) == 0:
                self.frame_locals(frame)
            else: 
                self.func_locals(frame)

            self.print_vars()
            self.clear()
        else:
            print('Type "locals help" for usage.')

    def _rec_prog_locals(self, func, rec_level):
        if func == None or rec_level > 5:
            return

        gdb.execute('b ' + func, to_string=True)
        if rec_level == 0:
            gdb.execute('r', to_string=True)
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
            
            operand = r'([xy]mm\d|\w+\sPTR\s[][\w+-]+|\w+)'
            res = re.search(r'.+(' + r'|'.join(ProgViewer.mov) + r')\s+' + operand + r',' + operand, line) # TODO: movs, movsb, movsw
            
            if res != None:
                components = res.groups()
                if re.search(r'(' + r'|'.join(ProgViewer.types) + r')\sPTR\s[][\w+-]+', components[1]) == None:
                    continue

                if components[0] == 'mov':
                     var_type = components[1].split(' ')[0]
                     c = self.get_var_format(var_type)
                elif components[0] == 'movss': # float
                    var_type = 'float'
                    c = 'f'
                elif components[0] == 'movsd': # double
                    var_type = 'double'
                    c = 'f'
                    
                stack_addr = components[1].split(' ')[2]
                stack_addr = stack_addr[1:len(stack_addr)-1]
                var_value  = components[2]

                var_addr = re.sub(r'\s+', r'', gdb.execute('x/{}x ${}'.format(c, stack_addr), to_string=True)).split(':')[0]                
                print('\t'*rec_level + '{:>14} {:>6} {:>15}'.format(var_addr, var_type, var_value))

            # TODO: check for fstp

    def prog_locals(self):
        self._rec_prog_locals('main', 0)

    def frame_locals(self, frame):
        disasm = gdb.execute('disassemble {}'.format(gdb.Frame.name(frame)), to_string=True).split('\n')
        for line in disasm:
            if '=>' in line:
                break

            operand = r'([xy]mm\d|\w+\sPTR\s[][\w+-]+|\w+)'
            res = re.search(r'.+(' + r'|'.join(ProgViewer.mov) + r')\s+' + operand + r',' + operand, line) # TODO: movs, movsb, movsw
            
            if res != None:
                components = res.groups()
                if re.search(r'(' + r'|'.join(ProgViewer.types) + r')\sPTR\s[][\w+-]+', components[1]) == None:
                    continue

                if components[0] == 'mov':
                     var_type = components[1].split(' ')[0]
                     c = self.get_var_format(var_type)
                elif components[0] == 'movss': # float
                    var_type = 'float'
                    c = 'f'
                elif components[0] == 'movsd': # double
                    var_type = 'double'
                    c = 'f'
                    
                stack_addr = components[1].split(' ')[2]
                stack_addr = stack_addr[1:len(stack_addr)-1]
                var_value  = components[2]

                var_addr, cur_val = re.sub(r'\s+', r'', gdb.execute('x/{}x ${}'.format(c, stack_addr), to_string=True)).split(':')                 
                self.vars[var_addr] = [var_type, var_value, cur_val]

            # TODO: check for fstp


    def get_var_format(self, var_type):
        if var_type == 'BYTE':
            return 'b'
        elif var_type == 'WORD':
            return 'h'
        elif var_type == 'DWORD':
            return 'w'
        elif var_type == 'QWORD' or var_type == 'TWORD':
            return 'g'

    def func_locals(self, frame):
        disasm = gdb.execute('disassemble {}'.format(gdb.Frame.name(frame)), to_string=True).split('\n')
        for line in disasm:
            operand = r'([xy]mm\d|\w+\sPTR\s[][\w+-]+|\w+)'
            res = re.search(r'.+(' + r'|'.join(ProgViewer.mov) + r')\s+' + operand + r',' + operand, line) # TODO: movs, movsb, movsw
            
            if res != None:
                components = res.groups()
                if re.search(r'(' + r'|'.join(ProgViewer.types) + r')\sPTR\s[][\w+-]+', components[1]) == None:
                    continue

                if components[0] == 'mov':
                     var_type = components[1].split(' ')[0]
                     c = self.get_var_format(var_type)
                elif components[0] == 'movss': # float
                    var_type = 'float'
                    c = 'f'
                elif components[0] == 'movsd': # double
                    var_type = 'double'
                    c = 'f'
                    
                stack_addr = components[1].split(' ')[2]
                stack_addr = stack_addr[1:len(stack_addr)-1]
                var_value  = components[2]

                var_addr, cur_val = re.sub(r'\s+', r'', gdb.execute('x/{}x ${}'.format(c, stack_addr), to_string=True)).split(':')                 
                self.vars[var_addr] = [var_type, var_value, cur_val]

            # TODO: check for fstp

    def clear(self):
        self.vars.clear()

    def print_nice_line(self):
        print('+=' + '='*14 + '=+=' + '='*6 + '=+=' + '='*15 + '=+=' + '='*18 + '=+')

    def print_vars(self):
        if len(self.vars) > 0:
            self.print_nice_line()
            print('| {:^14} | {:^6} | {:^15} | {:^18} |'.format('ADDRESS', 'TYPE', 'INITIAL_VALUE', 'CURRENT_VALUE'))
            self.print_nice_line()
            for var in self.vars:
                print('| {:>14} | {:>6} | {:>15} | {:>18} |'.format(var, self.vars[var][0], self.vars[var][1], self.vars[var][2]))
            self.print_nice_line()
        else:
            print('No variables detected')

ProgViewer()