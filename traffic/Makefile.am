EXTRA_DIST = ppp-traffic-analysis.py

bin_SCRIPTS = ppp-traffic-analysis.py

.PHONY: update
update: report.txt
	@cat report.txt

.PHONY: report.txt
report.txt: ppp-traffic-analysis.py ppp.log
	python $< ppp.log $@

# arch-tag: 65c713bc-f352-4534-b899-627b2cc1a9f5
