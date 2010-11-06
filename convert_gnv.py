#! /usr/bin/python

import sys, os;

def make_sgl_file(filename, vars_and_set):
    newfilename = filename + ".sgl";
    variables = vars_and_set[0].split(",");
    additional_polys = "";
    for var in variables:
        additional_polys += var + "^2+" + var + ",";
    sgl_string1 = "ring r=2,(" + vars_and_set[0] + "),dp;\n";
    sgl_string2 = "ideal I=" + additional_polys + vars_and_set[1][1:] + ";\n";
    sgl_string3 = """int t=timer;\nsystem("--ticks-per-sec",100);\noption(redSB);\nideal gb=groebner(I);\ntimer-t;\nexit;"""
    output = open(newfilename, "w");
    output.write(sgl_string1 + sgl_string2 + sgl_string3);
    output.close();

def make_coc_file(filename,vars_and_set):
    newfilename = filename + ".coc";
    variables = vars_and_set[0].split(",");
    analyzed_vars = {};
    additional_polys = "";
    for var in variables:
        additional_polys += var + "^2+" + var + ",";
        if var.isalpha():
            analyzed_vars[var] = [];
        else:
            if not analyzed_vars.has_key(var[:1]):
                analyzed_vars[var[:1]] = [];
            analyzed_vars[var[:1]].append(int(var[1:]));

    coc_string1 = "Use R::=Z/(2)[";
    for var in analyzed_vars.keys():
        if analyzed_vars[var]==[]:
            coc_string1 += var + ",";
        else:
            analyzed_vars[var].sort();
            if analyzed_vars[var][-1] - analyzed_vars[var][0] + 1 == len(analyzed_vars[var]):
                coc_string1 += var + "[" + str(analyzed_vars[var][0]) + ".." + str(analyzed_vars[var][-1]) + "],";
    coc_string1 = coc_string1[:-1] + "];\n";
    coc_string2 = "I:=Ideal(" + additional_polys + vars_and_set[1][1:] + ");";

    for var in analyzed_vars.keys():
        analyzed_vars[var].reverse();
        for n in analyzed_vars[var]:
            coc_string2 = coc_string2.replace(var + str(n), var + "[" + str(n) + "]");
    output = open(newfilename, "w");
    output.write(coc_string1 + coc_string2 + "G:=ReducedGBasis(I);\nQuit;");
    output.close();

def make_maple_file(filename,vars_and_set):
    newfilename = filename + ".mpl";
    variables = vars_and_set[0].split(",");
    additional_polys = "";
    for var in variables:
        additional_polys += var + "^2+" + var + ",";
    maple_string1 = "with(FGb):\nvars:=[" + vars_and_set[0] + "]:\n";
    maple_string2 = "polyset:=[" + additional_polys + vars_and_set[1][1:] + "]:\n";
    maple_string3 = "st:=time(): gb:=fgb_gbasis(polyset,2,vars,[]): time()-st;";
    output = open(newfilename, "w");
    output.write(maple_string1 + maple_string2 + maple_string3);
    output.close();

def make_dat_file(filename, vars_and_set):
    newfilename = filename + ".dat";
    variables_tmp = vars_and_set[0].split(",");
    variables = [];
    for i in range(len(variables_tmp)):
        variables.append('x' + str(i+1));

    number_of_variables = i + 1;
    polynoms = vars_and_set[1][1:];
    number_of_polynoms = polynoms.count(',') + 1;
    polynoms = polynoms.replace(",", "\n");
    for i in range(number_of_variables-1, -1, -1):
       polynoms = polynoms.replace(variables_tmp[i], variables[i]);
    polynoms = polynoms.replace("+", " + ");

    output = open(newfilename, "w");
    output.write(str(number_of_polynoms) + ' ' + str(number_of_variables) + '\n');
    output.write(polynoms);
    output.close();

def make_math_file(filename, vars_and_set):
    newfilename = filename + ".m";
    variables = vars_and_set[0].split(",");
    additional_polys = "";
    for var in variables:
        additional_polys += var + "^2+" + var + ",";
    sgl_string1 = "polys={" + additional_polys + vars_and_set[1][1:] + "};\n";
    sgl_string2 = "GroebnerBasis[polys,{" + vars_and_set[0] + "},Modulus->2];";
    output = open(newfilename, "w");
    output.write(sgl_string1 + sgl_string2);
    output.close();

def make_plbr_file(filename, vars_and_set):
    newfilename = filename + ".plbr";
    variables = vars_and_set[0].split(",");

    plbr_string1 = "change_ordering(dp_asc)\n";
    plbr_string2 = "groebner_basis([" + vars_and_set[1][1:] + "])\n";

    vars = []
    for var in variables:
        vars.append(var);
    vars.reverse();
    i = len(vars);
    for var in vars:
        plbr_string2 = plbr_string2.replace(var, "x(" + str(i) + ")");
        i -= 1;
    output = open(newfilename, "w");
    output.write(plbr_string1 + plbr_string2 + "exit()");
    output.close();

def make_mcl_file(filename, vars_and_set):
    newfilename = filename + ".mcl";
    variables = vars_and_set[0].split(",");
    mcl_string1 = """loadPackage "BooleanGB";\nR = ZZ/2[""" + vars_and_set[0] + ", MonomialOrder => GRevLex];\n";
    mcl_string2 = "J = apply(gens R, x -> x^2+x);\nQR = R/J;\n"
    mcl_string3 = "I = ideal(" + vars_and_set[1][1:] + ");\ntime C = gb I;\ntime B = gbBoolean I;\nassert(sort gens C - sort gens B == 0);";
    output = open(newfilename, "w");
    output.write(mcl_string1 + mcl_string2 + mcl_string3);
    output.close();

def make_target_file(target, filename, vars_and_set):
    if (target == "sgl"):
        make_sgl_file(filename, vars_and_set);
    elif (target == "coc"):
        make_coc_file(filename, vars_and_set);
    elif (target == "mpl"):
        make_maple_file(filename, vars_and_set);
    elif (target == "dat"):
        make_dat_file(filename, vars_and_set);
    elif (target == "math"):
        make_math_file(filename, vars_and_set);
    elif (target == "plbr"):
        make_plbr_file(filename, vars_and_set);
    elif (target == "mcl"):
        make_mcl_file(filename, vars_and_set);

def main():
    admissible = ["sgl", "coc", "mpl", "dat", "math", "plbr", "mcl"];
    targets = [];
    if (len(sys.argv) < 2):
        targets = ["mcl"];

    for i in range(1, len(sys.argv)):
        if sys.argv[i] in admissible:
            targets.append(sys.argv[i]);
        else:
            print "Unknown target format: '%s', ignoring it." % sys.argv[i];

    all_files = os.listdir(os.getcwd());
    for filename in all_files:
        if (filename[-3:] != "gnv"):
            continue;
        fn = open(filename, "r")
        data = fn.read().split(";")
        fn.close()
        example_name = filename[:-4];

        for target in targets:
            make_target_file(target, example_name, data);

if __name__ == "__main__":
    main();
