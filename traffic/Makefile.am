EXTRA_DIST  = ppp-traffic-analysis.py.in
bin_SCRIPTS = ppp-traffic-analysis.py
CLEANFILES  = ppp-traffic-analysis.py
ppp-traffic-analysis.py: ppp-traffic-analysis.py.in
	$(SED) \
		-e 's|[@]PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/ppp-traffic-analysis.py.in > ppp-traffic-analysis.py

.PHONY: update
update: report.txt
	@cat report.txt

.PHONY: report.txt
report.txt: ppp-traffic-analysis.py ppp.log
	python $< ppp.log $@
