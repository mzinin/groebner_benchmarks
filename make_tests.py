#!/usr/bin/python

import sys,os,string;

def cyclic(n):
    alst=[];
    allnums=range(n+1)[1:];
    for i in allnums:
        alst.append("x"+str(i));
    for i in allnums:
        alst.append("x"+str(i));

    out=open("cyclic"+str(n)+".gnv","w");
    for i in allnums[:-1]:
        out.write("x"+str(i)+",");
    out.write("x"+str(allnums[-1])+";\n");

    for i in range(n)[1:]:
        add="";
        for k in range(n+1)[1:]:
            mul="";
            for j in range(i+1)[1:]:
                mul+=alst[j+k-2]+"*";
            mul=mul[:-1];
            add+=mul+"+";
        add=add[:-1];
        out.write(add+",");

    mul="";
    for i in range(n+1)[1:]:
        mul+=alst[i-1]+"*";
    mul=mul[:-1]+"+1";
    out.write(mul+";\n1;");
    return "cyclic"+str(n)+".gnv";


def eco(n):
    allnums=range(n+1)[1:];
    out=open("eco"+str(n)+".gnv","w");
    for i in allnums[:-1]:
        out.write("x"+str(i)+",");
    out.write("x"+str(allnums[-1])+";\n");

    vars=["0"]
    for i in allnums:
        vars.append("x"+str(i));

    poly=""
    for i in allnums[:-1]:
        poly+=vars[i]+"+";
    poly+="1";
    out.write(poly+",");

    for i in allnums[:-2]:
        poly=vars[i]+"*"+vars[n]+"+";
        if (i%2):
            poly+="1+";
        for j in range(n-i)[1:]:
            poly+=vars[j]+"*"+vars[j+i]+"*"+vars[n]+"+";
        poly=poly[:-1]
        out.write(poly+",")

    i=n-1;
    poly=vars[i]+"*"+vars[n]+"+";
    if (i%2):
        poly+="1+";
    for j in range(n-i)[1:]:
        poly+=vars[j]+"*"+vars[j+i]+"*"+vars[n]+"+";
    poly=poly[:-1]
    out.write(poly+";\n1;")
    return "eco"+str(n)+".gnv"


def katsura(n):
    allnums=range(n+1);
    out=open("kats"+str(n)+".gnv","w");
    for i in allnums[:-1]:
        out.write("u"+str(i)+",");
    out.write("u"+str(allnums[-1])+";\n");

    vars=[]
    for i in allnums:
        vars.append("u"+str(i));

    poly=""
    for i in allnums:
        poly+=vars[i]+"+";
    poly+="1";
    out.write(poly+",");

    for i in allnums[1:-1]:
        poly="";
        present=[[0,i],[i]];
        for j in allnums[1:n-i+1]:
            t=[j,i+j];
            if t[0]==t[1]: t=t[:-1];
            t.sort();
            if t not in present: present.append(t);
        for j in allnums[1:i+1]:
            t=[j,i-j];
            if t[0]==t[1]: t=t[:-1];
            t.sort();
            if t not in present: present.append(t);
        for j in allnums[i+1:]:
            t=[j,j-i];
            if t[0]==t[1]: t=t[:-1];
            t.sort();
            if t not in present: present.append(t);
        for t in present:
            if len(t)==1:
                poly+=vars[t[0]]+"+";
            if len(t)==2:
                poly+=vars[t[0]]+"*"+vars[t[1]]+"+";
        poly=poly[:-1]+",";
        if i==n-1:
            poly=poly[:-1]+";\n1;"
        out.write(poly);
    return "kats"+str(n)+".gnv"


def fac(i):
    if (i==0 or i==1):
        return 1;
    else:
        res = 1;
        for t in range(i+1)[2:]:
            res*=t;
        return res;

def lcopy(lst):
    out=[];
    for i in range(len(lst)):
        out.append(lst[i]);
    return out;

def sim_poly(k,n):
    res=[];
    amount=fac(n)/fac(k)/fac(n-k);
    next=[];
    for i in range(k):
        next.append(i);
    res.append(lcopy(next));

    for i in range(amount-1):
        changing = k-1;
        while next[changing]==n-k+changing:
            changing-=1;
        next[changing]+=1;
        for j in range(changing+1,k):
            next[j]=next[j-1]+1;
        res.append(lcopy(next));

    out="";
    for i in range(len(res)):
        new="";
        for j in range(k):
            new+="x"+str(res[i][j])+"*";
        out+=new[:-1]+"+";
    return out[:-1];

def life(n):
    out=open("life"+str(n)+".gnv","w");
    for i in range(n):
        out.write("x"+str(i)+",");
    out.write("x"+str(n)+";\n");
        
    poly="x"+str(n)+"+"+sim_poly(n-2,n-1)+"+"+sim_poly(3,n-1);
    sub=sim_poly(n-2,n-1);
    poly+="+"+string.replace(sub,"+","*x"+str(n-1)+"+")+"*x"+str(n-1);

    sub=sim_poly(n-3,n-1);
    poly+="+"+string.replace(sub,"+","*x"+str(n-1)+"+")+"*x"+str(n-1);

    sub=sim_poly(3,n-1);
    poly+="+"+string.replace(sub,"+","*x"+str(n-1)+"+")+"*x"+str(n-1);

    sub=sim_poly(2,n-1);
    poly+="+"+string.replace(sub,"+","*x"+str(n-1)+"+")+"*x"+str(n-1);

    out.write(poly+";\n1;");
    return "life"+str(n)+".gnv";


def noon(n):
    allnums=range(n+1)[1:];
    out=open("noon"+str(n)+".gnv","w");
    for i in allnums[:-1]:
        out.write("x"+str(i)+",");
    out.write("x"+str(allnums[-1])+";\n");

    vars=["0"]
    for i in allnums:
        vars.append("x"+str(i));

    for i in allnums[:-1]:
        poly=vars[i]+"+";
        for j in range(i)[1:]:
            poly+=vars[i]+"*"+vars[j]+"+";
        for j in range(n+1)[i+1:]:
            poly+=vars[i]+"*"+vars[j]+"+";
        poly=poly[:-1]
        out.write(poly+",")

    i=n;
    poly=vars[i]+"+";
    for j in range(i)[1:]:
        poly+=vars[i]+"*"+vars[j]+"+";
    for j in range(n+1)[i+1:]:
        poly+=vars[i]+"*"+vars[j]+"+";
    poly=poly[:-1]
    out.write(poly+";\n");

    poly=""
    for i in allnums:
        poly+=vars[i]+"+";
    poly=poly[:-1];
    out.write(poly+";");
    return "noon"+str(n)+".gnv";


def redcyc(n):
    args=[];
    for i in range(n+1)[1:]:
        args.append("x"+str(i));
    args.append("z");
    out=open("redcyc"+str(n)+".gnv","w");

    for i in range(n+1)[1:]:
        out.write("x"+str(i)+",");
    out.write("z;\n");

    add="";
    for j in range(n+1)[1:]:
        add+=args[j-1]+"+";
    add+="1,";
    out.write(add);

    s=args[n]+"*";
    for i in range(n+1)[1:]:
        s+=args[i-1]+"*";
    s=s[:-1]+"+1,";
    out.write(s);

    add=args[0]+"*"+args[1]+"+"+args[0]+"+"+args[n-1]+"+";
    for j in range(n)[2:]:
        add+=args[j-1]+"*"+args[j]+"+";
    add=add[:-1]+",";
    out.write(add);

    for i in range(n)[3:]:
        s="";
        for j in range(i+1)[1:]:
            s+=args[j-1]+"*";
        f=s[:-1]+"+";
        s="";
        for j in range(i)[1:]:
            s+=args[j-1]+"*";
        f+=s[:-1]+"+";
        s=args[n-1]+"*";
        for j in range(i-1)[1:]:
            s+=args[j-1]+"*";
        f+=s[:-1]+"+";
        s=args[n-1]+"*";
        for j in range(n)[n+2-i:]:
            s+=args[j-1]+"*";
        f+=s[:-1]+",";
        out.write(f);

    i=n;
    s="";
    for j in range(i+1)[1:]:
        s+=args[j-1]+"*";
    f=s[:-1]+"+";
    s="";
    for j in range(i)[1:]:
        s+=args[j-1]+"*";
    f+=s[:-1]+"+";
    s=args[n-1]+"*";
    for j in range(i-1)[1:]:
        s+=args[j-1]+"*";
    f+=s[:-1]+"+";
    s=args[n-1]+"*";
    for j in range(n)[n+2-i:]:
        s+=args[j-1]+"*";
    f+=s[:-1]+";\n";
    out.write(f);

    out.write("1;");
    return "redcyc"+str(n)+".gnv";


def redeco(n):
    allnums=range(n+1)[1:];
    out=open("redeco"+str(n)+".gnv","w");
    for i in allnums[:-1]:
        out.write("x"+str(i)+",");
    out.write("x"+str(allnums[-1])+";\n");

    vars=["0"]
    for i in allnums:
        vars.append("x"+str(i));

    poly=""
    for i in allnums[:-1]:
        poly+=vars[i]+"+";
    poly+="1";
    out.write(poly+",");

    for i in allnums[:-2]:
        poly=vars[i]+"+"+vars[n]+"+";
        for j in range(n-i)[1:]:
            poly+=vars[j]+"*"+vars[j+i]+"+";
        poly=poly[:-1]
        out.write(poly+",")

    i=n-1;
    poly=vars[i]+"*"+vars[n]+"+";
    for j in range(n-i)[1:]:
        poly+=vars[j]+"*"+vars[j+i]+"+";
    poly=poly[:-1];
    out.write(poly+";\n1;");
    return "redeco"+str(n)+".gnv";


def make_sgl_file(filename):
    f=open(filename,"r");
    vars_and_set=f.read().split(";");
    f.close();
    
    newfilename=filename.split(".")[0]+".sgl";
    variables=vars_and_set[0].split(",");
    additional_polys="";
    for var in variables:
        additional_polys+=var+"^2+"+var+",";
    sgl_string1="ring r=2,("+vars_and_set[0]+"),dp;\n";
    sgl_string2="ideal I="+additional_polys+vars_and_set[1][1:]+";\n";
    sgl_string3="""int t=timer;\nsystem("--ticks-per-sec",100);\noption(redSB);\nideal gb=groebner(I);\ntimer-t;\nexit;"""
    output=open(newfilename,"w");
    output.write(sgl_string1+sgl_string2+sgl_string3);
    output.close();


def make_coc_file(filename):
    f=open(filename,"r");
    vars_and_set=f.read().split(";");
    f.close();
    
    newfilename=filename.split(".")[0]+".coc";
    variables=vars_and_set[0].split(",");
    analyzed_vars={};
    additional_polys="";
    for var in variables:
        additional_polys+=var+"^2+"+var+",";
        if var.isalpha():
            analyzed_vars[var]=[];
        else:
            if not analyzed_vars.has_key(var[:1]):
                analyzed_vars[var[:1]]=[];
            analyzed_vars[var[:1]].append(int(var[1:]));

    coc_string1="Use R::=Z/(2)[";
    for var in analyzed_vars.keys():
        if analyzed_vars[var]==[]:
            coc_string1+=var+",";
        else:
            analyzed_vars[var].sort();
            if analyzed_vars[var][-1]-analyzed_vars[var][0]+1==len(analyzed_vars[var]):
                coc_string1+=var+"["+str(analyzed_vars[var][0])+".."+str(analyzed_vars[var][-1])+"],";
    coc_string1=coc_string1[:-1]+"];\n";
    coc_string2="I:=Ideal("+additional_polys+vars_and_set[1][1:]+");";

    for var in analyzed_vars.keys():
        analyzed_vars[var].reverse();
        for n in analyzed_vars[var]:
            coc_string2=coc_string2.replace(var+str(n),var+"["+str(n)+"]");
    output=open(newfilename,"w");
    output.write(coc_string1+coc_string2+"G:=ReducedGBasis(I);\nQuit;");
    output.close();


def make_maple_file(filename):
    f=open(filename,"r");
    vars_and_set=f.read().split(";");
    f.close();
    
    newfilename=filename.split(".")[0]+".mpl";
    variables=vars_and_set[0].split(",");
    additional_polys="";
    for var in variables:
        additional_polys+=var+"^2+"+var+",";
    maple_string1="with(FGb):\nvars:=["+vars_and_set[0]+"]:\n";
    maple_string2="polyset:=["+additional_polys+vars_and_set[1][1:]+"]:\n";
    maple_string3="st:=time(): gb:=fgb_gbasis(polyset,2,vars,[]): time()-st;";
    output=open(newfilename,"w");
    output.write(maple_string1+maple_string2+maple_string3);
    output.close();


def func(name):
    if (name=="cyclic"):
        return cyclic;
    elif (name=="eco"):
        return eco;
    elif (name=="katsura"):
        return katsura;
    elif (name=="life"):
        return life;
    elif (name=="noon"):
        return noon;
    elif (name=="redcyc"):
        return redcyc;
    elif (name=="redeco"):
        return redeco;
    else:
        print "Unknown test\n";
        return fac;

def main():
    l = len(sys.argv);
    current_test = func(sys.argv[1]);
    n_begin = int(sys.argv[2]);
    if (n_begin<2): n_begin = 2;
    n_end = int(sys.argv[3]);

    admissible=['gnv','sgl','coc','mpl'];
    needed=[];
    for i in range(3,l):
        if sys.argv[i] in admissible:
            needed.append(sys.argv[i]);

    for i in range(n_begin, n_end+1):
        fn = current_test(i);
        if ('sgl' in needed):
            make_sgl_file(fn);
        if ('coc' in needed):
            make_coc_file(fn);
        if ('mpl' in needed):
            make_maple_file(fn);
        if ('gnv' not in needed):
            os.remove(fn);

if __name__=="__main__":
    main();

