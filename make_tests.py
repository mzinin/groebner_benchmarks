#!/usr/bin/env python3

import os
import sys


def cyclic(n):
    alst = []
    allnums = range(n + 1)[1:]
    for i in allnums:
        alst.append('x' + str(i))
    for i in allnums:
        alst.append('x' + str(i))

    out = open('cyclic' + str(n) + '.gnv', 'w')
    for i in allnums[:-1]:
        out.write('x' + str(i) + ',')
    out.write('x' + str(allnums[-1]) + ';\n')

    for i in range(n)[1:]:
        add = ''
        for k in range(n + 1)[1:]:
            mul = ''
            for j in range(i + 1)[1:]:
                mul += alst[j + k - 2] + '*'
            mul = mul[:-1]
            add += mul + '+'
        add = add[:-1]
        out.write(add + ',')

    mul = ''
    for i in range(n + 1)[1:]:
        mul += alst[i - 1] + '*'
    mul = mul[:-1] + '+1'
    out.write(mul + ';\n1;')

    return 'cyclic' + str(n) + '.gnv'


def eco(n):
    allnums = range(n + 1)[1:]
    out = open('eco' + str(n) + '.gnv', 'w')
    for i in allnums[:-1]:
        out.write('x' + str(i) + ',')
    out.write('x' + str(allnums[-1]) + ';\n')

    vars = ['0']
    for i in allnums:
        vars.append('x' + str(i))

    poly = ''
    for i in allnums[:-1]:
        poly += vars[i] + '+'
    poly += '1'
    out.write(poly + ',')

    for i in allnums[:-2]:
        poly = vars[i] + '*' + vars[n] + '+'
        if (i % 2 == 1):
            poly += '1+'
        for j in range(n - i)[1:]:
            poly += vars[j] + '*' + vars[j + i] + '*' + vars[n] + '+'
        poly = poly[:-1]
        out.write(poly + ',')

    i = n - 1
    poly = vars[i] + '*' + vars[n] + '+'
    if (i % 2 == 1):
        poly += '1+'
    for j in range(n - i)[1:]:
        poly += vars[j] + '*' + vars[j + i] + '*' + vars[n] + '+'
    poly = poly[:-1]
    out.write(poly + ';\n1;')
    return 'eco' + str(n) + '.gnv'


def katsura(n):
    allnums = range(n + 1)
    out = open('kats' + str(n) + '.gnv', 'w')
    for i in allnums[:-1]:
        out.write('u' + str(i) + ',')
    out.write('u' + str(allnums[-1]) + ';\n')

    vars = []
    for i in allnums:
        vars.append('u' + str(i))

    poly = ''
    for i in allnums:
        poly += vars[i] + '+'
    poly += '1'
    out.write(poly + ',')

    for i in allnums[1 : -1]:
        poly = ''
        present = [[0, i], [i]]

        for j in allnums[1 : n - i + 1]:
            t = [j, i + j]
            if t[0] == t[1]:
                t = t[:-1]
            t.sort()
            if t not in present:
                present.append(t)

        for j in allnums[1 : i + 1]:
            t = [j, i - j]
            if t[0] == t[1]:
                t = t[:-1]
            t.sort()
            if t not in present:
                present.append(t)

        for j in allnums[i + 1:]:
            t = [j, j - i]
            if t[0] == t[1]:
                t = t[:-1]
            t.sort()
            if t not in present:
                present.append(t)

        for t in present:
            if len(t) == 1:
                poly += vars[t[0]] + '+'
            if len(t) == 2:
                poly += vars[t[0]] + '*' + vars[t[1]] + '+'

        poly = poly[:-1] + ','
        if i == n - 1:
            poly = poly[:-1] + ';\n1;'
        out.write(poly)

    return 'kats' + str(n) + '.gnv'


def fac(i):
    if (i == 0 or i == 1):
        return 1
    else:
        res = 1
        for t in range(i + 1)[2:]:
            res *= t
        return res


def lcopy(lst):
    out = []
    for i in range(len(lst)):
        out.append(lst[i])
    return out


def sim_poly(k, n):
    res = []
    amount = int(fac(n) / fac(k) / fac(n - k))
    next = []
    for i in range(k):
        next.append(i)
    res.append(lcopy(next))

    for i in range(amount - 1):
        changing = k - 1
        while next[changing] == n - k + changing:
            changing -= 1
        next[changing] += 1

        for j in range(changing + 1, k):
            next[j] = next[j - 1] + 1
        res.append(lcopy(next))

    out = ''
    for i in range(len(res)):
        new = ''
        for j in range(k):
            new += 'x' + str(res[i][j]) + '*'
        out += new[:-1] + '+'
    return out[:-1]


def life(n):
    out = open('life' + str(n) + '.gnv', 'w')
    for i in range(n):
        out.write('x' + str(i) + ',')
    out.write('x' + str(n) + ';\n')

    poly = 'x' + str(n) + '+' + sim_poly(n - 2, n - 1) + '+' + sim_poly(3, n - 1)
    sub = sim_poly(n - 2, n - 1)
    poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

    sub = sim_poly(n - 3, n - 1)
    poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

    sub = sim_poly(3, n - 1)
    poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

    sub = sim_poly(2, n - 1)
    poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

    out.write(poly + ';\n1;')
    return 'life' + str(n) + '.gnv'


def noon(n):
    allnums = range(n + 1)[1:]
    out = open('noon' + str(n) + '.gnv', 'w')
    for i in allnums[:-1]:
        out.write('x' + str(i) + ',')
    out.write('x' + str(allnums[-1]) + ';\n')

    vars = ['0']
    for i in allnums:
        vars.append('x' + str(i))

    for i in allnums[:-1]:
        poly = vars[i] + '+'
        for j in range(i)[1:]:
            poly += vars[i] + '*' + vars[j] + '+'
        for j in range(n + 1)[i + 1:]:
            poly += vars[i] + '*' + vars[j] + '+'
        poly = poly[:-1]
        out.write(poly + ',')

    i = n
    poly = vars[i] + '+'
    for j in range(i)[1:]:
        poly += vars[i] + '*' + vars[j] + '+'
    for j in range(n + 1)[i + 1:]:
        poly += vars[i] + '*' + vars[j] + '+'
    poly = poly[:-1]
    out.write(poly + ';\n')

    poly = ''
    for i in allnums:
        poly += vars[i] + '+'
    poly = poly[:-1]
    out.write(poly + ';')
    return 'noon' + str(n) + '.gnv'


def redcyc(n):
    args = []
    for i in range(n + 1)[1:]:
        args.append('x' + str(i))
    args.append('z')
    out = open('redcyc' + str(n) + '.gnv', 'w')

    for i in range(n + 1)[1:]:
        out.write('x' + str(i) + ',')
    out.write('z;\n')

    add = ''
    for j in range(n + 1)[1:]:
        add += args[j - 1] + '+'
    add += '1,'
    out.write(add)

    s = args[n] + '*'
    for i in range(n + 1)[1:]:
        s += args[i - 1] + '*'
    s = s[:-1] + '+1,'
    out.write(s)

    add = args[0] + '*' + args[1] + '+' + args[0] + '+' + args[n-1] + '+'
    for j in range(n)[2:]:
        add += args[j - 1] + '*' + args[j] + '+'
    add = add[:-1] + ','
    out.write(add)

    for i in range(n)[3:]:
        s = ''
        for j in range(i + 1)[1:]:
            s += args[j - 1] + '*'
        f = s[:-1] + '+'
        s = ''
        for j in range(i)[1:]:
            s += args[j - 1] + '*'
        f += s[:-1] + '+'
        s = args[n - 1] + '*'
        for j in range(i - 1)[1:]:
            s += args[j - 1] + '*'
        f += s[:-1] + '+'
        s = args[n - 1] + '*'
        for j in range(n)[n + 2 - i:]:
            s += args[j - 1] + '*'
        f += s[:-1] + ','
        out.write(f)

    i = n
    s = ''
    for j in range(i + 1)[1:]:
        s += args[j - 1] + '*'
    f = s[:-1] + '+'

    s = ''
    for j in range(i)[1:]:
        s += args[j - 1] + '*'
    f += s[:-1] + '+'

    s = args[n - 1] + '*'
    for j in range(i - 1)[1:]:
        s += args[j-1] + '*'
    f += s[:-1] + '+'

    s = args[n - 1] + '*'
    for j in range(n)[n + 2 - i:]:
        s += args[j - 1] + '*'
    f += s[:-1] + ';\n'
    out.write(f)

    out.write('1;')
    return 'redcyc' + str(n) + '.gnv'


def redeco(n):
    allnums = range(n + 1)[1:]
    out = open('redeco' + str(n) + '.gnv', 'w')
    for i in allnums[:-1]:
        out.write('x' + str(i) + ',')
    out.write('x' + str(allnums[-1]) + ';\n')

    vars = ['0']
    for i in allnums:
        vars.append('x' + str(i))

    poly = ''
    for i in allnums[:-1]:
        poly += vars[i] + '+'
    poly += '1'
    out.write(poly + ',')

    for i in allnums[:-2]:
        poly = vars[i] + '+' + vars[n] + '+'
        for j in range(n - i)[1:]:
            poly += vars[j] + '*' + vars[j + i] + '+'
        poly = poly[:-1]
        out.write(poly + ',')

    i = n - 1
    poly = vars[i] + '*' + vars[n] + '+'
    for j in range(n - i)[1:]:
        poly += vars[j] + '*' + vars[j + i] + '+'
    poly = poly[:-1]
    out.write(poly + ';\n1;')
    return 'redeco' + str(n) + '.gnv'


def make_singular_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '.sgl'
    variables = vars_and_set[0].split(',')
    additional_polys = ''
    for var in variables:
        additional_polys += var + '^2+' + var + ','
    sgl_string1 = 'ring r=2,(' + vars_and_set[0] + '),dp;\n'
    sgl_string2 = 'ideal I=' + additional_polys + vars_and_set[1][1:] + ';\n'
    sgl_string3 = 'int t=timer;\nsystem("--ticks-per-sec",100);\noption(redSB);\nideal gb=groebner(I);\ntimer-t;\nexit;'
    output = open(newfilename, 'w')
    output.write(sgl_string1 + sgl_string2 + sgl_string3)
    output.close()


def make_cocoa_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '.coc'
    variables = vars_and_set[0].split(',')
    analyzed_vars = {}
    additional_polys = ''
    for var in variables:
        additional_polys += var + '^2+' + var + ','
        if var.isalpha():
            analyzed_vars[var] = []
        else:
            if var[:1] not in analyzed_vars:
                analyzed_vars[var[:1]] = []
            analyzed_vars[var[:1]].append(int(var[1:]))

    coc_string1 = 'Use R::=Z/(2)['
    for var in analyzed_vars.keys():
        if analyzed_vars[var] == []:
            coc_string1 += var + ','
        else:
            analyzed_vars[var].sort()
            if analyzed_vars[var][-1] - analyzed_vars[var][0] + 1 == len(analyzed_vars[var]):
                coc_string1 += var + '[' + str(analyzed_vars[var][0]) + '..' + str(analyzed_vars[var][-1]) + '],'
    coc_string1 = coc_string1[:-1] + '];\n'
    coc_string2 = 'I:=Ideal(' + additional_polys + vars_and_set[1][1:] + ');'

    for var in analyzed_vars.keys():
        analyzed_vars[var].reverse()
        for n in analyzed_vars[var]:
            coc_string2 = coc_string2.replace(var + str(n), var + '[' + str(n) + ']')
    output = open(newfilename, 'w')
    output.write(coc_string1 + coc_string2 + 'G:=ReducedGBasis(I);\nQuit;')
    output.close()


def make_maple_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '.mpl'
    variables = vars_and_set[0].split(',')
    additional_polys = ''
    for var in variables:
        additional_polys += var + '^2+' + var + ','
    maple_string1 = 'with(FGb):\nvars:=[' + vars_and_set[0] + ']:\n'
    maple_string2 = 'polyset:=[' + additional_polys + vars_and_set[1][1:] + ']:\n'
    maple_string3 = 'st:=time(): gb:=fgb_gbasis(polyset,2,vars,[]): time()-st;'
    output = open(newfilename, 'w')
    output.write(maple_string1 + maple_string2 + maple_string3)
    output.close()


def make_dat_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '.dat'
    variables_tmp = vars_and_set[0].split(',')
    variables = []
    for i in range(len(variables_tmp)):
        variables.append('x' + str(i + 1))

    number_of_variables = i + 1
    polynoms = vars_and_set[1][1:]
    number_of_polynoms = polynoms.count(',') + 1
    polynoms = polynoms.replace(',', '\n')
    for i in range(number_of_variables - 1, -1, -1):
       polynoms = polynoms.replace(variables_tmp[i], variables[i])
    polynoms = polynoms.replace('+', ' + ')

    output = open(newfilename, 'w')
    output.write(str(number_of_polynoms) + ' ' + str(number_of_variables) + '\n')
    output.write(polynoms)
    output.close()


def make_mathematica_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '.m'
    variables = vars_and_set[0].split(',')
    additional_polys = ''
    for var in variables:
        additional_polys += var + '^2+' + var + ','

    sgl_string1 = 'polys={' + additional_polys + vars_and_set[1][1:] + '};\n'
    sgl_string2 = 'GroebnerBasis[polys,{' + vars_and_set[0] + '},Modulus->2];'

    output = open(newfilename, 'w')
    output.write(sgl_string1 + sgl_string2)
    output.close()


def make_polybori_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '.plbr'
    variables = vars_and_set[0].split(',')

    plbr_string1 = 'change_ordering(dp_asc)\n'
    plbr_string2 = 'groebner_basis([' + vars_and_set[1][1:] + '])\n'

    vars = []
    for var in variables:
        vars.append(var)
    vars.reverse()
    i = len(vars)
    for var in vars:
        plbr_string2 = plbr_string2.replace(var, 'x(' + str(i) + ')')
        i -= 1
    output = open(newfilename, 'w')
    output.write(plbr_string1 + plbr_string2 + 'exit()')
    output.close()


def make_macaulay_bibasis_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '_bibasis.mcl'
    variables = vars_and_set[0].split(',')
    mcl_string1 = 'loadPackage "BIBasis";\nR = ZZ/2[' + vars_and_set[0] + ', MonomialOrder => GRevLex];\n'
    mcl_string2 = 'I = ideal(' + vars_and_set[1][1:] + ');\ntime biBasis(I);'
    output = open(newfilename, 'w')
    output.write(mcl_string1 + mcl_string2)
    output.close()


def make_macaulay_gb_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '_gb.mcl'
    variables = vars_and_set[0].split(',')
    mcl_string1 = 'R = ZZ/2[' + vars_and_set[0] + ', MonomialOrder => GRevLex];\n'
    mcl_string2 = 'J = apply(gens R, x -> x^2+x);\nQR = R/J;\n'
    mcl_string3 = 'I = ideal(' + vars_and_set[1][1:] + ');\ntime G = gb(I);\ngens(G);'

    output = open(newfilename, 'w')
    output.write(mcl_string1 + mcl_string2 + mcl_string3)
    output.close()


def make_macaulay_gbboolean_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '_gbboolean.mcl'
    variables = vars_and_set[0].split(',')
    mcl_string1 = 'loadPackage "BooleanGB";\nR = ZZ/2[' + vars_and_set[0] + ', MonomialOrder => GRevLex];\n'
    mcl_string2 = 'I = ideal(' + vars_and_set[1][1:] + ');\ntime gbBoolean(I);'
    output = open(newfilename, 'w')
    output.write(mcl_string1 + mcl_string2)
    output.close()


def make_reduce_bibasis_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '_bibasis.rdc'
    variables = vars_and_set[0].split(',')
    rdc_string1 = 'load_package "bibasis"$\n'
    rdc_string2 = 'vars := {' + vars_and_set[0] + '}$\n'
    rdc_string3 = 'polys := {' + vars_and_set[1][1:].replace(',', ',\n') + '}$\n'
    rdc_string4 = 'bibasis(polys, vars, degrevlex, t);\nbibasis_print_statistics();\nquit;\n'

    output = open(newfilename, 'w')
    output.write(rdc_string1 + rdc_string2 + rdc_string3 + rdc_string4)
    output.close()


def make_reduce_groebner_file(filename):
    f = open(filename, 'r')
    vars_and_set = f.read().split(';')
    f.close()

    newfilename = filename.split('.')[0] + '_groebner.rdc'
    variables = vars_and_set[0].split(',')
    additional_polys = ''
    for var in variables:
        additional_polys += var + '**2+' + var + ','

    variables = vars_and_set[0].split(',')
    rdc_string1 = 'load_package "groebner"$\non modular$\nsetmod 2$\non time$\n'
    rdc_string2 = 'torder({' + vars_and_set[0] + '}, revgradlex)$\n'
    rdc_string3 = 'groebner({' + (additional_polys + vars_and_set[1][1:]).replace(',', ',\n') + '});\n'
    rdc_string4 = 'quit;\n'

    output = open(newfilename, 'w')
    output.write(rdc_string1 + rdc_string2 + rdc_string3 + rdc_string4)
    output.close()


def func(name):
    if (name == 'cyclic'):
        return cyclic
    elif (name == 'eco'):
        return eco
    elif (name == 'katsura'):
        return katsura
    elif (name == 'life'):
        return life
    elif (name == 'noon'):
        return noon
    elif (name == 'redcyc'):
        return redcyc
    elif (name == 'redeco'):
        return redeco
    else:
        print('Unknown test: ' + name + '\n')
        return fac


def usage(script_name):
    print('Usage: ' + script_name + ' <benchmark> <start> <end> [application]*')
    print('   benchmark   = cyclic | eco | katsura | life | noon | redcyc | redeco - name of benchmark,')
    print('   start       - integer >= 2, first benchmark in generated series,')
    print('   end         - integer >= start, last benchmark in generated series,')
    print('   application = gnv | sgl | coc | mpl | dat | math | plbr | mcl_bibasis | mcl_gb | mcl_gbboolean | rdc_bibasis | rdc_groebner - software package the benchmarks will be generated for.')
    print('Example: ' + script_name + ' life 6 15 gnv mpl sgl')


def main():
    l = len(sys.argv)
    if (l < 4):
        usage(sys.argv[0])
        return

    current_test = func(sys.argv[1])
    n_begin = int(sys.argv[2])
    if (n_begin < 2):
        n_begin = 2
    n_end = int(sys.argv[3])

    admissible = ['gnv', 'sgl', 'coc', 'mpl', 'dat', 'math', 'plbr',
                  'mcl_bibasis', 'mcl_gb', 'mcl_gbboolean', 'rdc_bibasis', 'rdc_groebner']
    needed = []
    for i in range(3, l):
        if sys.argv[i] in admissible:
            needed.append(sys.argv[i])

    for i in range(n_begin, n_end + 1):
        fn = current_test(i)
        if ('sgl' in needed):
            make_singular_file(fn)
        if ('coc' in needed):
            make_cocoa_file(fn)
        if ('mpl' in needed):
            make_maple_file(fn)
        if ('dat' in needed):
            make_dat_file(fn)
        if ('math' in needed):
            make_mathematica_file(fn)
        if ('plbr' in needed):
            make_polybori_file(fn)
        if ('mcl_bibasis' in needed):
            make_macaulay_bibasis_file(fn)
        if ('mcl_gb' in needed):
            make_macaulay_gb_file(fn)
        if ('mcl_gbboolean' in needed):
            make_macaulay_gbboolean_file(fn)
        if ('rdc_bibasis' in needed):
            make_reduce_bibasis_file(fn)
        if ('rdc_groebner' in needed):
            make_reduce_groebner_file(fn)
        if ('gnv' not in needed):
            os.remove(fn)

if __name__ == '__main__':
    main()
