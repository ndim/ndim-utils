# ndim's utilities

ndim's collection of miscellaneous mixed utilities written for use by
the author.

If you also find those utilities useful, feel free to use them.


## Utilities

Some of those are ancient and not very useful, others suitable for
daily use.

  * admin-py/

    Some admin tools written in python. Mostly whois and DNS stuff.

  * cdburn/

    Burn CDs without clicking and remembering all those options.

  * misc/

    Miscellaneous helpers programs.

  * misc-scripts/

    Miscellanrous scripts.

  * palm-scripts/

    Hotplug scripts for using a Palm device (upload, backup, PPP).

  * params/

    Print information on how the program has been called.

  * pkg-info/

    Information about the ndim-utils package.

  * traffic/

    Analyze ppp logs from a LEAF Bering router.


## Build and install

      /---------------------------------------------\

	./autogen.mk
	./configure \
		--prefix="$HOME/root/ndim-utils"
	make
	make install

      \---------------------------------------------/

Then I have a few symlinks to the scripts installed to
`$HOME/root/ndim-utils/bin` in some places.


## Stuff to fix

  * seperate independent parts into independent modules
    (e.g. the palm hotplug scripts)
