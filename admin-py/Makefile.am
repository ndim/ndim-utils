EXTRA_DIST = whois.py whois-tool.py whoislist setup.py.in
DISTCLEANFILES = timestamp.sh

nameservers: domain-list $(srcdir)/whois-tool.py whoislist
	python2 whois-check.py $< $@.new
	mv $@.new $@

MAINTAINERCLEAN_FILES = whoislist.gz
EXTRA_DIST += whoislist.gz
whoislist.gz:
	if test ! -s whoislist.gz && test -s "$(srcdir)/whoislist.gz"; then \
		cp "$(srcdir)/whoislist.gz" $@; \
	else \
		wget -O $@ "http://www.geektools.com/dist/whoislist.gz"; \
	fi

whoislist: whoislist.gz
	gunzip -c < $< > $@

whois.html: whois.py
	pydoc -w whois

BUILT_SOURCES = timestamp.stamp

timestamp.stamp:
	echo -e '#!/bin/sh\necho "whois-stuff-$(shell date -I)"' > timestamp.sh

TARBASE = $$(sh timestamp.sh)

.PHONY: myclean
myclean:
	rm -f *~
	rm -f "$(TARBASE).tar.gz"
	rm -f "$(TARBASE)/"*
	-rmdir "$(TARBASE)"

.PHONY: mydist
mydist: $(TARBASE).tar.gz

$(TARBASE).tar.gz: Makefile $(srcdir)/whois-check.py whoislist domain-list
	mkdir "$(TARBASE)"
	cp $^ "$(TARBASE)/"
	tar cvfz $@ --owner=root --group=root "$(TARBASE)/"
	rm "$(TARBASE)/"*
	rmdir "$(TARBASE)"

# arch-tag: 37ae571d-6f90-4e57-8548-ef1e0eddb24b
