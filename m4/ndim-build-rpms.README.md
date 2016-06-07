How to use `ndim-build-rpms.m4` and `ndim-build-rpms.mk`
--------------------------------------------------------

In `${top_srcdir}/configure.ac`:

    AM_INIT_AUTOMAKE([ ... dist-xz ... ])
    ...
    m4_pattern_forbid([NDIM_BUILD_RPMS])dnl
    NDIM_BUILD_RPMS()dnl
    ...
    AC_CONFIG_FILES...
    AC_OUTPUT

In `${top_srcdir}/Makefile.am`:

    CLEAN_LOCAL_TARGETS = ...
    CLEANFILES = ...
    EXTRA_DIST = ...
    ...
    include m4/ndim-build-rpms.mk
    ...
    clean-local: $(CLEAN_LOCAL_TARGETS)

The file `${top_srcdir}/package.spec.in` must contain a basic RPM spec
file with some specific names to be subsituted by the rule in
`ndim-build-rpms.mk`.

Then you can run either of the two following commands:

  1. Build source and binary RPM packages on the local system:

         [user@host ~/my-src]$ make rpm

     The resulting RPM files will be found in the `rpm-dist`
     subdirectory.

  2. Build source and binary RPM package(s) in a mock chroot
     environment (requires the local system is a Fedora installation):

         [user@host ~/my-src]$ make mockbuild

     The resulting RPM files will be found in the `results_PACKAGE`
     subdirectory.


How it works
------------

Running `make dist` will generate a `PACKAGE.tar.xz` package tarball
and a `PACKAGE.spec` RPM spec file.

Running `make rpm` will run `rpmbuild` to build RPMs from these two
files on the local machine.

Running `make mockbuild` will run `fedpkg mockbuild` to build RPMs
from these two files in a mock chroot environment.
