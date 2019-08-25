#!/usr/bin/env python3

import math
import os
import sys


def cyclic(n):
    output_filename = 'cyclic{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        allnums = range(1, n + 1)
        alst = ['x{}'.format(i) for i in allnums]
        alst *= 2

        output.write(','.join(['x{}'.format(i) for i in allnums]))
        output.write(';\n')

        polynoms = []

        for i in range(n)[1:]:
            add = ''
            for k in range(n + 1)[1:]:
                mul = ''
                for j in range(i + 1)[1:]:
                    mul += alst[j + k - 2] + '*'
                mul = mul[:-1]
                add += mul + '+'
            polynoms.append(add[:-1])

        mul = ''
        for i in range(n + 1)[1:]:
            mul += alst[i - 1] + '*'
        polynoms.append(mul[:-1] + '+1')

        output.write(','.join(polynoms))
        output.write(';\n1;')

    return output_filename


def eco(n):
    output_filename = 'eco{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        allnums = range(1, n + 1)
        vars = ['x{}'.format(i) for i in range(n + 1)]

        output.write(','.join(vars[1:]))
        output.write(';\n')

        polynoms = []

        polynom = '+'.join([vars[i] for i in allnums[:-1]]) + '+1'
        polynoms.append(polynom)

        for i in allnums[:-1]:
            polynom = vars[i] + '*' + vars[n] + '+' + ('1+' if i % 2 == 1 else '')
            polynom += '+'.join([vars[j] + '*' + vars[j + i] + '*' + vars[n] for j in range(1, n - i)])
            if polynom[-1] == '+':
                polynom = polynom[:-1]
            polynoms.append(polynom)

        output.write(','.join(polynoms))
        output.write(';\n1;')

    return output_filename


def katsura(n):
    output_filename = 'kats{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        allnums = range(n + 1)
        vars = ['u{}'.format(i) for i in range(n + 1)]

        output.write(','.join(vars))
        output.write(';\n')

        polynoms = []

        polynom = '+'.join(vars) + '+1'
        polynoms.append(polynom)

        for i in allnums[1 : -1]:
            polynom = ''
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
                    polynom += vars[t[0]] + '+'
                if len(t) == 2:
                    polynom += vars[t[0]] + '*' + vars[t[1]] + '+'

            polynoms.append(polynom[:-1])

        output.write(','.join(polynoms))
        output.write(';\n1;')

    return output_filename


def sim_poly(k, n):
    next = [i for i in range(k)]
    res = [next.copy()]

    amount = int(math.factorial(n) / math.factorial(k) / math.factorial(n - k))

    for i in range(amount - 1):
        changing = k - 1
        while next[changing] == n - k + changing:
            changing -= 1
        next[changing] += 1

        for j in range(changing + 1, k):
            next[j] = next[j - 1] + 1
        res.append(next.copy())

    out = []
    for i in range(len(res)):
        new = '*'.join(['x{}'.format(res[i][j]) for j in range(k)])
        out.append(new)

    return '+'.join(out)


def life(n):
    output_filename = 'life{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        output.write(','.join(['x{}'.format(i) for i in range(n + 1)]))
        output.write(';\n')

        poly = 'x' + str(n) + '+' + sim_poly(n - 2, n - 1) + '+' + sim_poly(3, n - 1)
        sub = sim_poly(n - 2, n - 1)
        poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

        sub = sim_poly(n - 3, n - 1)
        poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

        sub = sim_poly(3, n - 1)
        poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

        sub = sim_poly(2, n - 1)
        poly += '+' + sub.replace('+', '*x' + str(n - 1) + '+') + '*x' + str(n - 1)

        output.write(poly)
        output.write(';\n1;')

    return output_filename


def noon(n):
    output_filename = 'noon{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        allnums = range(1, n + 1)
        vars = ['x{}'.format(i) for i in range(n + 1)]

        output.write(','.join(vars[1:]))
        output.write(';\n')

        polynoms = []

        for i in allnums:
            polynom = vars[i] + '+'
            polynom += '+'.join([vars[i] + '*' + vars[j] for j in range(1, i)])
            polynom += '+' if polynom[-1] != '+' else ''
            polynom += '+'.join([vars[i] + '*' + vars[j] for j in range(i + 1, n + 1)])
            if polynom[-1] == '+':
                polynom = polynom[:-1]
            polynoms.append(polynom)

        output.write(','.join(polynoms))
        output.write(';\n')

        polynom = '+'.join([vars[i] for i in allnums])
        output.write(polynom)
        output.write(';')

    return output_filename


def redcyc(n):
    output_filename = 'redcyc{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        args = ['x{}'.format(i) for i in range(1, n + 1)]
        args.append('z')

        output.write(','.join(args))
        output.write(';\n')

        polynoms = []

        add = '+'.join([args[j - 1] for j in range(1, n + 1)])
        add += '+1'
        polynoms.append(add)

        s = '*'.join([args[i - 1] for i in range(1, n + 2)])
        s += '+1'
        polynoms.append(s)

        add = args[0] + '*' + args[1] + '+' + args[0] + '+' + args[n - 1] + '+'
        add += '+'.join([args[j - 1] + '*' + args[j] for j in range(2, n)])
        polynoms.append(add)

        for i in range(3, n + 1):
            s = '*'.join([args[j - 1] for j in range(1, i + 1)])
            f = s + '+'

            s = '*'.join([args[j - 1] for j in range(1, i)])
            f += s + '+'

            s = args[n - 1] + '*'
            s += '*'.join([args[j - 1] for j in range(1, i - 1)])
            f += s + '+'

            s = args[n - 1] + '*'
            s += '*'.join([args[j - 1] for j in range(n + 2 - i, n)])
            f += s

            polynoms.append(f)

        output.write(','.join(polynoms))
        output.write(';\n1;')

    return output_filename


def redeco(n):
    output_filename = 'redeco{}.gnv'.format(n)

    with open(output_filename, 'w') as output:
        allnums = range(1, n + 1)
        vars = ['x{}'.format(i) for i in range(n + 1)]

        output.write(','.join(vars[1:]))
        output.write(';\n')

        polynoms = []

        polynom = '+'.join([vars[i] for i in allnums[:-1]])
        polynom += '+1'
        polynoms.append(polynom)

        for i in allnums[:-1]:
            polynom = vars[i] + ('+' if i != n - 1 else '*') + vars[n] + '+'
            polynom += '+'.join([vars[j] + '*' + vars[j + i] for j in range(1, n - i)])
            if polynom[-1] == '+':
                polynom = polynom[:-1]
            polynoms.append(polynom)

        output.write(','.join(polynoms))
        output.write(';\n1;')

    return output_filename


def read_gnv_content(filename):
    with open(filename, 'r') as input:
        variables, polynoms, _ = input.read().split(';', 2)
        return variables.strip().split(','), polynoms.strip()


def make_singular_file(filename):
    output_filename = os.path.splitext(filename)[0] + '.sgl'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        output.write('ring r=2,({}),dp;\n'.format(','.join(variables)))
        output.write('ideal I={},{};\n'.format(','.join(additional_polys), polynoms))
        output.write('int t=timer;\n')
        output.write('system("--ticks-per-sec",100);\n')
        output.write('option(redSB);\n')
        output.write('ideal gb=groebner(I);\n')
        output.write('timer-t;\n')
        output.write('exit;')


def make_cocoa_file(filename):
    output_filename = os.path.splitext(filename)[0] + '.coc'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        analyzed_vars = {}
        for var in variables:
            if var.isalpha():
                analyzed_vars[var] = []
            else:
                if var[:1] not in analyzed_vars:
                    analyzed_vars[var[:1]] = []
                analyzed_vars[var[:1]].append(int(var[1:]))

        ring_vars = []
        for var in analyzed_vars.keys():
            if analyzed_vars[var] == []:
                ring_vars.append(var)
            else:
                analyzed_vars[var].sort()
                if analyzed_vars[var][-1] - analyzed_vars[var][0] + 1 == len(analyzed_vars[var]):
                    ring_vars.append('{}[{}..{}]'.format(var, analyzed_vars[var][0], analyzed_vars[var][-1]))

        output.write('Use R::=Z/(2)[{}];\n'.format(','.join(ring_vars)))

        ideal = '{},{}'.format(','.join(additional_polys), polynoms)
        for var in analyzed_vars.keys():
            analyzed_vars[var].reverse()
            for n in analyzed_vars[var]:
                ideal = ideal.replace('{}{}'.format(var, n), '{}[{}]'.format(var, n))

        output.write('I:=Ideal({});\n'.format(ideal))
        output.write('G:=ReducedGBasis(I);\n'.format(ideal))
        output.write('Quit;'.format(ideal))


def make_maple_file(filename):
    output_filename = os.path.splitext(filename)[0] + '.mpl'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        output.write('with(FGb):\n')
        output.write('vars:=[{}]:\n'.format(','.join(variables)))
        output.write('polyset:=[{},{}]:\n'.format(','.join(additional_polys), polynoms))
        output.write('st:=time():\n')
        output.write('gb:=fgb_gbasis(polyset,2,vars,[]):\n')
        output.write('time()-st;')


def make_dat_file(filename):
    output_filename = os.path.splitext(filename)[0] + '.dat'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)

        dat_variables = ['x{}'.format(i + 1) for i in range(len(variables))]
        number_of_variables = len(dat_variables)
        number_of_polynoms = polynoms.count(',') + 1
        polynoms = polynoms.replace(',', '\n')

        for i in range(number_of_variables - 1, -1, -1):
            polynoms = polynoms.replace(variables[i], dat_variables[i])
        polynoms = polynoms.replace('+', ' + ')

        output.write('{} {}\n'.format(number_of_polynoms, number_of_variables))
        output.write(polynoms)


def make_mathematica_file(filename):
    output_filename = os.path.splitext(filename)[0] + '.m'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        output.write('polys={{{},{}}};\n'.format(','.join(additional_polys), polynoms))
        output.write('GroebnerBasis[polys,{{{}}},Modulus->2];'.format(','.join(variables)))


def make_polybori_file(filename):
    output_filename = os.path.splitext(filename)[0] + '.plbr'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)

        for i in range(len(variables) - 1, -1, -1):
            polynoms = polynoms.replace(variables[i], 'x({})'.format(i + 1))

        output.write('change_ordering(dp_asc)\n')
        output.write('groebner_basis([{}])\n'.format(polynoms))
        output.write('exit()')


def make_macaulay_bibasis_file(filename):
    output_filename = os.path.splitext(filename)[0] + '_bibasis.mcl'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)

        output.write('loadPackage "BIBasis";\n')
        output.write('R = ZZ/2[{}, MonomialOrder => GRevLex];\n'.format(','.join(variables)))
        output.write('I = ideal({});\n'.format(polynoms))
        output.write('time biBasis(I);')


def make_macaulay_gb_file(filename):
    output_filename = os.path.splitext(filename)[0] + '_gb.mcl'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)

        output.write('R = ZZ/2[{}, MonomialOrder => GRevLex];\n'.format(','.join(variables)))
        output.write('J = apply(gens R, x -> x^2+x);\n')
        output.write('QR = R/J;\n')
        output.write('I = ideal({});\n'.format(polynoms))
        output.write('time G = gb(I);\n')
        output.write('gens(G);')


def make_macaulay_gbboolean_file(filename):
    output_filename = os.path.splitext(filename)[0] + '_gbboolean.mcl'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)

        output.write('loadPackage "BooleanGB";\n')
        output.write('R = ZZ/2[{}, MonomialOrder => GRevLex];\n'.format(','.join(variables)))
        output.write('I = ideal({});\n'.format(polynoms))
        output.write('time gbBoolean(I);')


def make_reduce_bibasis_file(filename):
    output_filename = os.path.splitext(filename)[0] + '_bibasis.rdc'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)

        output.write('load_package "bibasis"$\n')
        output.write('vars := {{{}}}$\n'.format(','.join(variables)))
        output.write('polys := {{{}}}$\n'.format(polynoms.replace(',', ',\n')))
        output.write('bibasis(polys, vars, degrevlex, t);\n')
        output.write('bibasis_print_statistics();\n')
        output.write('quit;\n')


def make_reduce_groebner_file(filename):
    output_filename = os.path.splitext(filename)[0] + '_groebner.rdc'

    with open(output_filename, 'w') as output:
        variables, polynoms = read_gnv_content(filename)
        additional_polys = ['{0}**2+{0}'.format(var) for var in variables]

        output.write('load_package "groebner"$\n')
        output.write('on modular$\n')
        output.write('setmod 2$\n')
        output.write('on time$\n')
        output.write('torder({{{}}}, revgradlex)$\n'.format(','.join(variables)))
        output.write('groebner({{{},{}}});\n'.format(','.join(additional_polys), polynoms.replace(',', ',\n')))
        output.write('quit;\n')


def usage(script_name):
    print(script_name + ' generates benchmarks for computing boolean Groebner bases in various software packages.\n')
    print('Usage: ' + script_name + ' <benchmark> <start> <end> [format]*')
    print('   benchmark = cyclic | eco | katsura | life | noon | redcyc | redeco - name of benchmark,')
    print('   start     - integer >= 2, first benchmark in generated series,')
    print('   end       - integer >= start, last benchmark in generated series,')
    print('   format    = gnv | sgl | coc | mpl | dat | math | plbr | mcl_bibasis | mcl_gb | mcl_gbboolean | rdc_bibasis | rdc_groebner' + \
          ' - software package\'s format the benchmarks will be generated for.\n')
    print('Example: ' + script_name + ' life 6 15 gnv mpl sgl\n')


def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])
        sys.exit(1)

    benchmarks = { 'cyclic': cyclic,
                   'eco': eco,
                   'katsura': katsura,
                   'life': life,
                   'noon': noon,
                   'redcyc': redcyc,
                   'redeco': redeco }

    formats = { 'gnv': lambda x: None,
                'sgl': make_singular_file,
                'coc': make_cocoa_file,
                'mpl': make_maple_file,
                'dat': make_dat_file,
                'math': make_mathematica_file,
                'plbr': make_polybori_file,
                'mcl_bibasis': make_macaulay_bibasis_file,
                'mcl_gb': make_macaulay_gb_file,
                'mcl_gbboolean': make_macaulay_gbboolean_file,
                'rdc_bibasis': make_reduce_bibasis_file,
                'rdc_groebner': make_reduce_groebner_file }

    current_benchmark = sys.argv[1]
    if current_benchmark not in benchmarks:
        print('Unsupported benchmark: ' + current_benchmark + '\n')
        sys.exit(1)

    n_begin = int(sys.argv[2]) if int(sys.argv[2]) >= 2 else 2
    n_end = int(sys.argv[3])

    output_formats = set()
    for i in range(3, len(sys.argv)):
        if sys.argv[i] in formats:
            output_formats.add(sys.argv[i])

    for i in range(n_begin, n_end + 1):
        gnv_file = benchmarks[current_benchmark](i)

        for output_format in output_formats:
            formats[output_format](gnv_file)

        if 'gnv' not in output_formats:
            os.remove(gnv_file)


if __name__ == '__main__':
    main()
