
AM_CPPFLAGS = -I${top_srcdir} -I${top_builddir}

this_includedir=${includedir}/${subdir}
this_include_HEADERS = \
    all.hpp \
    armijo.hpp \
    constraint.hpp \
    costfunction.hpp \
    endcriteria.hpp \
    levenbergmarquardt.hpp \
    linesearch.hpp \
    lmdif.hpp \
    method.hpp \
    problem.hpp

libOptimization_la_SOURCES = \
    armijo.cpp \
    constraint.cpp \
    endcriteria.cpp \
    levenbergmarquardt.cpp \
    linesearch.cpp \
    lmdif.cpp

noinst_LTLIBRARIES = libOptimization.la

all.hpp: Makefile.am
	echo "/* This file is automatically generated; do not edit.     */" > $@
	echo "/* Add the files to be included into Makefile.am instead. */" >> $@
	echo >> $@
	for i in $(filter-out all.hpp, $(this_include_HEADERS)); do \
		echo "#include <${subdir}/$$i>" >> $@; \
	done
	echo >> $@
	subdirs='$(SUBDIRS)'; for i in $$subdirs; do \
		echo "#include <${subdir}/$$i/all.hpp>" >> $@; \
	done

