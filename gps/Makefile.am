PATH := $(HOME)/root/gpspoint/bin:$(PATH)
LD_LIBRARY_PATH := $(HOME)/root/gpspoint/lib:$(LD_LIBRARY_PATH)
export PATH LD_LIBRARY_PATH

EXTRA_DIST = geocoord.py pop-z61.raw-route utmlist2gpd.py guntool.py setup.py

#.PHONY: all
#all: pop-z61.gpd
#	cat $^

#.PHONY: backup
#backup:

%.gpd: %.raw-route utmlist2gpd.py geocoord.py
	python utmlist2gpd.py $< $@ $*.clean-route

DEVOPT = -dev /dev/ttyS0 -rec Garmin -prot NMEA

%.save.wp:
	gpsman -log $(DEVOPT) getwrite WP gpsman $@

%.save.tr:
	gpsman -log $(DEVOPT) getwrite TR gpsman $@

%.save.rt:
	gpsman -log $(DEVOPT) getwrite RT gpsman $@

%.upload.wp: %.wp
	gpsman -log $(DEVOPT) readput gpsman $< WP

%.upload.rt: %.rt
	gpsman -log $(DEVOPT) readput gpsman $< RT

%.upload.tr: %.tr
	gpsman -log $(DEVOPT) readput gpsman $< TR

# arch-tag: 3aa8af8b-bb7e-43b6-9020-62abb8c98115
