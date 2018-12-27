def parseC(code):
    code = [i.strip() for i in code.split('\n')]
    arg = {}
    topArg = None
    varArg = []
    for i in code:
        if 'lua_to' in i:
            I = i
            try:
                id = int(i.partition('lua_to')[2].split()[1][0])
            except ValueError:
                id = None
            i = i.split()
            if '=' in i:
                t = i.index('=')
                name = i[t-1]
                if t >= 2:
                    type = i[t-2].rstrip('*')
                elif i[t+1][0] == '*':
                    type = i[t+1][2:-3]
                else:
                    type = I.partition('lua_to')[2].split()[0][:-3]
            else:
                t = [j for j in range(len(i)) if 'lua_to' in i[j]][0]
                if t > 0 and i[t-1][0] == '*':
                    type = i[t-1][2:-3]
                else:
                    type = I.partition('lua_to')[0][:-2]
        elif 'check_param' in i:
            if 'check_param_count' in i:
                id = int(i[21])
                type = None
                name = None
            else:
                i = i.partition('check_param')[2].split()
                try:
                    id = int(i[2][0])
                except ValueError:
                    id = None
                type = i[1][11:-1].lower()
                name = None
        elif 'lua_is' in i:
            try:
                i = i.partition('lua_is')[2].split()
                id = int(i[1][0])
            except ValueError:
                id = None
            type = i[0][6:-3]
            name = None
        elif 'lua_gettop' in i:
            i = i.split()
            if '=' in i:
                topArg = i[i.index('=')-1]
            else:
                topArg = None
            continue
        elif '2value' in i:
            id = 0
            type = i[13:i.find('2value')]
            name = None
        elif 'lua_push' in i:
            id = 0
            i = i[i.find('lua_push'):].split('(')
            type = i[0][8:]
            name = None
        elif 'lua_yield' in i:
            id = 0
            type = None
            name = None
        else:
            continue
        if id is None:
            varArg.append((type, name))
        elif id in arg:
            arg[id].append((type, name))
        else:
            arg[id] = [(type, name)]
    if topArg:
        arg[max(arg, default=1)].append(('uint32', topArg))
    return arg, varArg

def fmtArg(arg, name=True):
    if not arg: return '??? ???'
    a = [i for i in set(i[0] for i in arg) if i]
    b = [i for i in set(i[1] for i in arg) if i]
    return ('|'.join(a) if len(a)>0 else '???') + (' ' + ('|'.join(b) if len(b)>0 else '???') if name else '')

def genDoc(group, name, parse):
    arg, varArg = parse
    doc  = '●' + (fmtArg(arg[0], False) if 0 in arg else 'void') + ' ' + group + '.' + name + '('
    doc += ', '.join(fmtArg(arg[i] if i in arg else None) for i in range(1, max(arg, default=0)+1))
    doc += ')'
    if varArg:
        doc += '\n variable position arguments: ' + str(varArg)
    return doc

from re import findall, DOTALL

lua2c = dict(findall('"([A-Za-z]*)", scriptlib::([a-z_]*)', open('interpreter.cpp').read()))
c2card = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libcard.cpp').read(), flags=DOTALL))
c2duel = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libduel.cpp').read(), flags=DOTALL))
c2debug = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libdebug.cpp').read(), flags=DOTALL))
c2effect = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libeffect.cpp').read(), flags=DOTALL))
c2group = dict(findall('scriptlib::([a-z_]*)\(lua_State \* ?L\) \{\n(.*?)\n}', open('libgroup.cpp').read(), flags=DOTALL))

for i,j in lua2c.items():
    group = j.partition('_')[0]
    print(genDoc(group[0].upper()+group[1:], i, parseC(globals()['c2'+group][j])))