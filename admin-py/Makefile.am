EXTRA_DIST = whois.py whois-tool.py whoislist setup.py.in
DISTCLEANFILES = whoislist.gz

nameservers: domain-list whois-tool.py whoislist
	python2 whois-check.py $< $@.new
	mv $@.new $@

whoislist.gz:
	wget -O $@ "http://www.geektools.com/dist/whoislist.gz"

whoislist: whoislist.gz
	gunzip -c < $< > $@

whois.html: whois.py
	pydoc -w whois

TARBASE := whois-stuff-$(shell date -I)

.PHONY: myclean
myclean:
	rm -f *~
	rm -f $(TARBASE).tar.gz
	rm -f $(TARBASE)/*
	-rmdir $(TARBASE)

.PHONY: mydist
mydist: $(TARBASE).tar.gz

$(TARBASE).tar.gz: Makefile whois-check.py whoislist domain-list
	mkdir $(TARBASE)
	cp $^ $(TARBASE)/
	tar cvfz $@ --owner=root --group=root $(TARBASE)/
	rm $(TARBASE)/*
	rmdir $(TARBASE)

# arch-tag: 37ae571d-6f90-4e57-8548-ef1e0eddb24b
