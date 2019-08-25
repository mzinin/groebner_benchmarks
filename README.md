# Boolean Gröbner Benchmarks

This is a collection of benchmarks for computing boolean [Gröbner bases](https://en.wikipedia.org/wiki/Gröbner_basis). The collection contains benchmarks in CNF and GNV format. Also there are two Python scripts for generating benchmark series and for converting GNV files into formats used by some 3rd party Computer Algebra packages.


## CNF files

CNF stands for Conjunctive Normal Form. This format is commonly used by [DIMACS](http://dimacs.rutgers.edu/), its description can be found [here](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html);


## GNV files

GNV name if related to [GINV project](http://invo.jinr.ru/ginv/index.html), which got its name as short for "Gröbner Involutive". Please pay attention that GNV format and GINV project share only some resemblance in their names. GNV files are not suitable for GINV in any way.

### GNV format

This format is very simple. A GNV file contains 3 sections in the following strict order:

* comma-separated list of independant variables
* comma-separated list of polynomials (a.k.a. initial basis)
* and comma-separated list of correct answer (a.k.a. boolean Gröbner basis)

Each section must end with semicolon. All white spaces and new line symbols are ignored.

Example:
```
x0,x1,x2,x3,x4;
x4+x0*x1+x0*x2+x1*x2+x0*x1*x2+x0*x1*x3+x0*x2*x3+x1*x2*x3+x0*x3+x1*x3+x2*x3+x0*x1*x2*x3+x0*x1*x3+x0*x2*x3+x1*x2*x3;
x2*x3*x4+x0*x3+x1*x3+x0*x4+x1*x4+x2*x4,
x1*x3*x4+x0*x3+x2*x3+x0*x4+x1*x4+x2*x4,
x0*x3*x4+x1*x3+x2*x3+x0*x4+x1*x4+x2*x4,
x1*x2*x4+x0*x1+x0*x2+x0*x4+x1*x4+x2*x4+x4,
x0*x2*x4+x0*x1+x1*x2+x0*x4+x1*x4+x2*x4+x4,
x0*x1*x4+x0*x2+x1*x2+x0*x4+x1*x4+x2*x4+x4,
x1*x2*x3+x0*x1+x0*x2+x0*x3+x1*x4+x2*x4+x3*x4,
x0*x2*x3+x0*x1+x1*x2+x1*x3+x0*x4+x2*x4+x3*x4,
x0*x1*x3+x0*x2+x1*x2+x2*x3+x0*x4+x1*x4+x3*x4,
x0*x1*x2+x0*x1+x0*x2+x1*x2+x0*x4+x1*x4+x2*x4+x4;
```


## make_tests.py

This Python 3 script can be used to generate series of benchmarks in GNV format and other formats supported by other Computer Algebra systems.

To get help message just run `make_tests.py` without any arguments:
```
$ ./make_tests.py
./make_tests.py generates benchmarks for computing boolean Groebner bases in various software packages.

Usage: ./make_tests.py <benchmark> <start> <end> [format]*
   benchmark = cyclic | eco | katsura | life | noon | redcyc | redeco - name of benchmark,
   start     - integer >= 2, first benchmark in generated series,
   end       - integer >= start, last benchmark in generated series,
   format    = gnv | sgl | coc | mpl | dat | math | plbr | mcl_bibasis | mcl_gb | mcl_gbboolean | rdc_bibasis | rdc_groebner - software package's format the benchmarks will be generated for.

Example: ./make_tests.py life 6 15 gnv mpl sgl
```

The supported output formats are:

* `gnv` - already mentioned [GNV format](#gnv-format)
* `sgl` - scripr file for [Singular](https://www.singular.uni-kl.de/)
* `coc` - script file for [CoCoA System](http://cocoa.dima.unige.it/)
* `mpl` - script for [Maple](https://www.maplesoft.com/products/maple/) with [FGb](https://www-polsys.lip6.fr/~jcf/FGb/index.html) package
* `dat` - shame on me, I do not remeber how to use those dat files
* `math` - script for [Mathematica](http://www.wolfram.com/mathematica/)
* `plbr` - script for [PolyBoRi](http://polybori.sourceforge.net/) (it seems the project is dead already)
* `mcl_bibasis` - script for [Macaulay2](http://www2.macaulay2.com/Macaulay2/) to compute Gröbner basis with [BIBasis](https://faculty.math.illinois.edu/Macaulay2/doc/Macaulay2-1.14/share/doc/Macaulay2/BIBasis/html/) package
* `mcl_gb` - script for [Macaulay2](http://www2.macaulay2.com/Macaulay2/) to compute Gröbner basis with builtin `gb` function
* `mcl_gbboolean` - script for [Macaulay2](http://www2.macaulay2.com/Macaulay2/) to compute Gröbner basis with [BooleanGB](https://faculty.math.illinois.edu/Macaulay2/doc/Macaulay2-1.14/share/doc/Macaulay2/BooleanGB/html/) package
* `rdc_bibasis` - script for [REDUCE](http://www.reduce-algebra.com/) to compute Gröbner basis with [BIBASIS](http://www.reduce-algebra.com/manual/contributed/bibasis.pdf) package
* `rdc_groebner` - script for [REDUCE](http://www.reduce-algebra.com/) to compute Gröbner basis with [GROEBNER](http://www.reduce-algebra.com/manual/contributed/groebner.pdf) package


## convert_gnv.py

Asit follows from its name this Python 3 script just converts all GNV files in the current directory into other formats.

To get help run the script without any arguments:
```
$ ./convert_gnv.py
./convert_gnv.py converts all GNV benchmarks in the current directory into third party software packages formats.

Usage: ./convert_gnv.py [format]*
   format    = sgl | coc | mpl | dat | math | plbr | mcl_bibasis | mcl_gb | mcl_gbboolean | rdc_bibasis | rdc_groebner - software package's format the benchmarks will be generated for.

Example: ./convert_gnv.py mpl sgl
```

The list of the supported output formats is the same as for the `make_tests.py` script.
