# Instrument software for the Low Resolution Imaging Spectrograph 2 (LRIS2)

include ./Mk.instrument

override SYSNAM = kss/$(INSTRUMENT)/
override VERNUM = 1.0


DIRS = init.d
# hardware servers
DIRS += l2power

#  won't build until after other services are installed.
DIRS += 




## qt needs Qt.
# DIRS += qt

################################################################################
# KROOT boilerplate:
# Include general make rules, using default values for the key environment
# variables if they are not already set.

ifndef KROOT
	KROOT = /kroot
endif

ifndef RELNAM
	RELNAM = default
endif

ifndef RELDIR
	RELDIR = $(KROOT)/rel/$(RELNAM)
endif

include $(KROOT)/etc/config.mk
################################################################################
