#!/usr/bin/env python3

import os
import sys


def make_singular_file(path, variables, polynoms):
    output_filename = path + '.sgl'

    with open(output_filename, 'w') as output:
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        output.write('ring r=2,({}),dp;\n'.format(','.join(variables)))
        output.write('ideal I={},{};\n'.format(','.join(additional_polys), polynoms))
        output.write('int t=timer;\n')
        output.write('system("--ticks-per-sec",100);\n')
        output.write('option(redSB);\n')
        output.write('ideal gb=groebner(I);\n')
        output.write('timer-t;\n')
        output.write('exit;')


def make_cocoa_file(path, variables, polynoms):
    output_filename = path + '.coc'

    with open(output_filename, 'w') as output:
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


def make_maple_file(path, variables, polynoms):
    output_filename = path + '.mpl'

    with open(output_filename, 'w') as output:
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        output.write('with(FGb):\n')
        output.write('vars:=[{}]:\n'.format(','.join(variables)))
        output.write('polyset:=[{},{}]:\n'.format(','.join(additional_polys), polynoms))
        output.write('st:=time():\n')
        output.write('gb:=fgb_gbasis(polyset,2,vars,[]):\n')
        output.write('time()-st;')


def make_dat_file(path, variables, polynoms):
    output_filename = path + '.dat'

    with open(output_filename, 'w') as output:
        dat_variables = ['x{}'.format(i + 1) for i in range(len(variables))]
        number_of_variables = len(dat_variables)
        number_of_polynoms = polynoms.count(',') + 1
        polynoms = polynoms.replace(',', '\n')

        for i in range(number_of_variables - 1, -1, -1):
            polynoms = polynoms.replace(variables[i], dat_variables[i])
        polynoms = polynoms.replace('+', ' + ')

        output.write('{} {}\n'.format(number_of_polynoms, number_of_variables))
        output.write(polynoms)


def make_mathematica_file(path, variables, polynoms):
    output_filename = path + '.m'

    with open(output_filename, 'w') as output:
        additional_polys = ['{0}^2+{0}'.format(var) for var in variables]

        output.write('polys={{{},{}}};\n'.format(','.join(additional_polys), polynoms))
        output.write('GroebnerBasis[polys,{{{}}},Modulus->2];'.format(','.join(variables)))


def make_polybori_file(path, variables, polynoms):
    output_filename = path + '.plbr'

    with open(output_filename, 'w') as output:
        for i in range(len(variables) - 1, -1, -1):
            polynoms = polynoms.replace(variables[i], 'x({})'.format(i + 1))

        output.write('change_ordering(dp_asc)\n')
        output.write('groebner_basis([{}])\n'.format(polynoms))
        output.write('exit()')


def make_macaulay_bibasis_file(path, variables, polynoms):
    output_filename = path + '_bibasis.mcl'

    with open(output_filename, 'w') as output:
        output.write('loadPackage "BIBasis";\n')
        output.write('R = ZZ/2[{}, MonomialOrder => GRevLex];\n'.format(','.join(variables)))
        output.write('I = ideal({});\n'.format(polynoms))
        output.write('time biBasis(I);')


def make_macaulay_gb_file(path, variables, polynoms):
    output_filename = path + '_gb.mcl'

    with open(output_filename, 'w') as output:
        output.write('R = ZZ/2[{}, MonomialOrder => GRevLex];\n'.format(','.join(variables)))
        output.write('J = apply(gens R, x -> x^2+x);\n')
        output.write('QR = R/J;\n')
        output.write('I = ideal({});\n'.format(polynoms))
        output.write('time G = gb(I);\n')
        output.write('gens(G);')


def make_macaulay_gbboolean_file(path, variables, polynoms):
    output_filename = path + '_gbboolean.mcl'

    with open(output_filename, 'w') as output:
        output.write('loadPackage "BooleanGB";\n')
        output.write('R = ZZ/2[{}, MonomialOrder => GRevLex];\n'.format(','.join(variables)))
        output.write('I = ideal({});\n'.format(polynoms))
        output.write('time gbBoolean(I);')


def make_reduce_bibasis_file(path, variables, polynoms):
    output_filename = path + '_bibasis.rdc'

    with open(output_filename, 'w') as output:
        output.write('load_package "bibasis"$\n')
        output.write('vars := {{{}}}$\n'.format(','.join(variables)))
        output.write('polys := {{{}}}$\n'.format(polynoms.replace(',', ',\n')))
        output.write('bibasis(polys, vars, degrevlex, t);\n')
        output.write('bibasis_print_statistics();\n')
        output.write('quit;\n')


def make_reduce_groebner_file(path, variables, polynoms):
    output_filename = path + '_groebner.rdc'

    with open(output_filename, 'w') as output:
        additional_polys = ['{0}**2+{0}'.format(var) for var in variables]

        output.write('load_package "groebner"$\n')
        output.write('on modular$\n')
        output.write('setmod 2$\n')
        output.write('on time$\n')
        output.write('torder({{{}}}, revgradlex)$\n'.format(','.join(variables)))
        output.write('groebner({{{},{}}});\n'.format(','.join(additional_polys), polynoms.replace(',', ',\n')))
        output.write('quit;\n')


def read_gnv_content(filename):
    with open(filename, 'r') as input:
        variables, polynoms, _ = input.read().split(';', 2)
        return variables.strip().split(','), polynoms.strip()


def usage(script_name):
    print(script_name + ' converts all GNV benchmarks in the current directory into third party software packages formats.\n')
    print('Usage: ' + script_name + ' [format]*')
    print('   format    = sgl | coc | mpl | dat | math | plbr | mcl_bibasis | mcl_gb | mcl_gbboolean | rdc_bibasis | rdc_groebner' + \
          ' - software package\'s format the benchmarks will be generated for.\n')
    print('Example: ' + script_name + ' mpl sgl\n')


def main():
    if len(sys.argv) < 2:
        usage(sys.argv[0])
        sys.exit(1)

    formats = { 'sgl': make_singular_file,
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

    output_formats = set()
    for i in range(1, len(sys.argv)):
        if sys.argv[i] in formats:
            output_formats.add(sys.argv[i])

    for filename in os.listdir(os.getcwd()):
        path, extension = os.path.splitext(filename)
        if extension != '.gnv':
            continue

        variables, polynoms = read_gnv_content(filename)

        for output_format in output_formats:
            formats[output_format](path, variables, polynoms)


if __name__ == '__main__':
    main()
