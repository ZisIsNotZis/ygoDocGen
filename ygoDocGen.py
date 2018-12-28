def parseC(code):
    code = [i.strip() for i in code.split('\n')]
    arg = {}
    nArg = None
    varArg = []
    for i in code:
        if 'lua_to' in i:
            I = i
            id = i.partition('lua_to')[2].split()[1].split(')')[0]
            try: id = int(id)
            except ValueError: pass
            i = i.split()
            if '=' in i:
                t = i.index('=')
                name = i[t-1]
                if i[t+1][0] == '*':
                    Type = i[t+1][2:-3]
                else:
                    Type = I.partition('lua_to')[2].partition(' ')[0][:-3]
            else:
                t = [j for j in range(len(i)) if 'lua_to' in i[j]][0]
                name = None
                Type = I.partition('lua_to')[2].split()[0][:-3]
        elif 'check_param' in i:
            if 'check_param_count' in i:
                nArg = int(i[21:-2])
                continue
            else:
                i = i.partition('check_param')[2].split()
                id = i[2].partition(')')[0].split(',')[0]
                try: id = int(id)
                except ValueError: pass
                Type = i[1][11:-1].lower()
                name = None
        elif 'lua_is' in i:
            i = i.partition('lua_is')[2].split()
            id = i[1].partition(')')[0]
            try: id = int(id)
            except ValueError: pass
            Type = i[0][:-3]
            name = None
        elif 'get_function_handle' in i:
            id = int(i.partition('get_function_handle')[2].split(')')[0][4:])
            Type = 'function'
            i = i.split()
            if '=' in i:
                name = i[i.index('=')-1]
            else:
                name = None
        elif '2value' in i:
            id = 0
            Type = i[13:i.find('2value')]
            name = None
        elif 'lua_push' in i:
            id = 0
            i = i[i.find('lua_push'):].split('(')
            Type = i[0][8:]
            name = None
        elif 'lua_yield' in i:
            id = 0
            Type = None
            name = None
        else:
            continue
        if type(id) is str:
            varArg.append((Type, name))
        elif id in arg:
            arg[id].append((Type, name))
        else:
            arg[id] = [(Type, name)]
    if nArg and not varArg:
        arg[nArg].append((None, None))
    return arg, varArg, nArg

trans = dict(integer='int',
             boolean='bool',
             function='fn',
             value='int')

def fmtArg(arg, ret=False, nil='?'):
    if arg:
        a = [translate[i] if i in translate else i for i in set(i[0] for i in arg) if i]
        b = [i.split('>')[-1] for i in set(i[1] for i in arg) if i]
    else:
        a = []
        b = []
    return ('|'.join(a) if len(a)>0 else 'nil' if ret else nil) + ' ' + ('' if ret else ('|'.join(b) if len(b)>0 else nil))

def genDoc(name, parse):
    arg, varArg, nArg = parse
    doc = '●' + fmtArg(arg[0] if 0 in arg else None, True) + name + '('
    arg = [fmtArg(arg[i] if i in arg else None) for i in range(1, max(arg, default=0)+1)]
    if varArg:
        arg.append(fmtArg(varArg) + '...')
    if nArg and len(arg) > nArg:
        arg = arg[:nArg] + ['[' + ', '.join(arg[nArg:]) + ']']
    doc += ', '.join(arg) + ')'
    return doc

from re import findall, DOTALL

lua2c = findall('"([A-Za-z]*)", scriptlib::([a-z_]*)', open('interpreter.cpp').read())
c2card = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libcard.cpp').read(), flags=DOTALL))
c2duel = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libduel.cpp').read(), flags=DOTALL))
c2debug = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libdebug.cpp').read(), flags=DOTALL))
c2effect = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libeffect.cpp').read(), flags=DOTALL))
c2group = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libgroup.cpp').read(), flags=DOTALL))
t = open('_functions.txt',encoding='utf-8-sig').read()
t = re.sub('===+[^=]*=*\n', '', t)
old = dict((j,i) for i,j in findall('●([^ ]* ([^(]*)[^\n]*\n[^●]*)\n', t, DOTALL))

for i,j in lua2c:
    group = j.partition('_')[0]
    name = group[0].upper() + group[1:] + '.' + i
    print(genDoc(name, parseC(globals()['c2'+group][j])))
    if name in old:
        print('', old[name].replace('\n','\n '))
