EXTRA_DIST = ppp-traffic-analysis.py

bin_SCRIPTS = ppp-traffic-analysis.py

.PHONY: update
update: report.txt
	@cat report.txt

.PHONY: report.txt
report.txt: ppp-traffic-analysis.py ppp.log
	python $< ppp.log $@
