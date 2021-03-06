#
# makefile.in - Input makefile for the configure script.
#

SHELL = /bin/sh

#### Start of system configuration section. ####

prefix = /usr/local
exec_prefix = ${prefix}

bindir = ${exec_prefix}/bin
libdir = /usr/local/lib64
includedir = ${prefix}/include

INSTALLDIRS =\
$(bindir)\
$(libdir)\
$(includedir)

DISTDIR = ~/pub_web

INSTALL = /usr/bin/install -c
INSTALL_PROGRAM = ${INSTALL}
INSTALL_DATA = ${INSTALL} -m 644

NOCOMPLEX = 
HAVE_GRIDNODES_H = 

CC = /usr/bin/gcc34
CFLAGS = -g -O2 -Wall -m64 -fPIC
CFLAGS_TRIANGLE = -g -O2 -Wall -w -ffloat-store
LDFLAGS = -L/usr/local/lib64

AR = ar
ARFLAGS = cru

LIBS = -lgu -lm 

MLIB = -lm

#### end of configuration section ####

SRC =\
broyden.c\
delaunay.c\
geom.c\
gridgen.c\
hash.c\
issimplepoly.c\
istack.c\
ode.c\
swcr.c\
vertlist.c\
zode.c

HEADERS =\
broyden.h\
delaunay.h\
geom.h\
gridgen.h\
hash.h\
issimplepoly.h\
istack.h\
nan.h\
ode.h\
swcr.h\
version.h\
vertlist.h\
zode.h

ifeq ($(NOCOMPLEX),yes)
  COMPLEXSRC =\
  c99-min/clog.c\
  c99-min/cmplx.c\
  c99-min/stubs.c
endif

LIBSRC=$(SRC) $(COMPLEXSRC)

LIBOBJS = $(LIBSRC:.c=.o)

SLIBOBJS = $(LIBSRC:.c=.t)
%.t: %.c
	$(CC) $(CFLAGS) -fPIC -c $*.c -o $*.t

all: gridgen
	@if [ ! -f libgridgen.a ] ; then \
	   echo "  type 'make lib' to make libgridgen.a"; \
	fi
	@if [ ! -f libgridgen.so ] ; then \
	   echo "  type 'make shlib' to make libgridgen.so"; \
	fi

lib: libgridgen.a

shlib: libgridgen.so

gridgen: main.c $(HEADERS) $(SRC) triangle.o
	$(CC) -o gridgen -DGRIDGEN_STANDALONE $(CFLAGS) main.c $(SRC) triangle.o $(LDFLAGS) $(MLIB)

tests: avl.c broyden.c issimplepoly.c hash.c
	$(CC) -o test_avl avl.c -DTEST_AVL $(CFLAGS) -I. $(MLIB)
	$(CC) -o test_broyden broyden.c -DTEST_BROYDEN $(CFLAGS) -I. $(MLIB)
	$(CC) -o issimplepoly issimplepoly.c -DTEST_SI $(CFLAGS) -I. $(MLIB)
	$(CC) -o test_hash hash.c -DHT_TEST $(CFLAGS) -I. $(MLIB)

standalone: override CFLAGS+=-static
standalone: gridgen tests
	strip gridgen
	strip issimplepoly

libgridgen.a: $(HEADERS) triangle.o $(LIBOBJS)
	$(AR) $(ARFLAGS) $@ $(LIBOBJS) triangle.o
	chmod go+r $@

libgridgen.so: $(HEADERS) triangle.t $(SLIBOBJS)
	rm -f $@
	$(CC) -shared -o $@ $(SLIBOBJS) triangle.t $(LIBS)

triangle.o: triangle.c
	$(CC) -c -DTRILIBRARY $(CFLAGS_TRIANGLE) -I. triangle.c

triangle.t: triangle.c
	$(CC) -c -DTRILIBRARY $(CFLAGS_TRIANGLE) -fPIC -I. triangle.c -o triangle.t

installdirs: $(INSTALLDIRS)
	@$(SHELL) mkinstalldirs $(INSTALLDIRS)

install: all installdirs
	@for i in gridgen; do \
	   echo "  installing $$i"; \
	   fname=`basename $$i`; \
	   $(INSTALL_PROGRAM) $$i $(bindir); \
	done
	@for i in gridgen.h; do \
	   echo "  installing $$i"; \
	   $(INSTALL_DATA) $$i $(includedir); \
	done
	@for i in libgridgen.a libgridgen.so; do \
	   if test -f $$i; then \
	      echo "  installing $$i"; \
	      $(INSTALL_DATA) $$i $(libdir)/$$i; \
	   fi \
	done

clean:
	rm -f *.o *.t c99-min/*.o *.a *.so *~ \#*\# core gridgen issimplepoly test_broyden test_hash test_avl

configclean:
	rm -f config.h makefile config.cache config.status config.log

distclean: clean configclean

indent:
	indent -T FILE -T swcr -T vertnode -T vertlist -T edge -T quadrilateral -T gridgen -T odestruct -T calcstruct -T zdouble -T point -T delaunay -T istack -T triangle -T DIRECTION -T endpoint -T endpointtqueue -T slseg -T segnode -T sweepline  -T DIRECTION -T VISIT -T SIBLING_ORDER -T NODETYPE -T ht_bucket -T hashtable main.c $(SRC) $(HEADERS)
	rm -f *~

dist:
	WDIR=`pwd`;\
	DIR=`basename $$WDIR`;\
	cp -r $$WDIR /tmp;\
	cd /tmp/$$DIR/examples;\
	make clean;\
	cd /tmp/$$DIR;\
	rm -rf `find /tmp/$$DIR -name CVS`;\
	if [ -e makefile ] ; then\
		make distclean;\
	fi;\
	/tmp/"$$DIR"/configure;\
	make standalone;\
	chmod a+r+x gridgen;\
	chmod a+r+x issimplepoly;\
	mv -f gridgen $(DISTDIR);\
	mv -f issimplepoly $(DISTDIR);\
	make distclean;\
	cd $(DISTDIR);\
	mv -f $$DIR".tar.gz" $$DIR".tar.gz.prev";\
	gzip -f gridgen;\
	gzip -f issimplepoly;\
	cd /tmp;\
	tar czvf $$DIR".tar.gz" $$DIR;\
	chmod a+r $$DIR".tar.gz";\
	mv -f $$DIR".tar.gz" $(DISTDIR)/$$DIR".tar.gz";\
	rm -rf $$DIR
