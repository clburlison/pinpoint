# Makefile for pinpoint pre/postflight package creation

PKGTITLE="pinpoint-script"
PKGVERSION="1.0"
PKGID="com.clburlison.pinpoint-script"
PROJECT="pinpoint"

#################################################

##Help - Show this help menu
help: 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##  setup - Create the working directory and script
setup:
	mkdir -p pkgroot/Library/Application\ Support/pinpoint
	touch pkgroot/Library/Application\ Support/pinpoint/preflight
	touch pkgroot/Library/Application\ Support/pinpoint/postflight
	chmod 744 pkgroot/Library/Application\ Support/pinpoint/*flight

##  clean - Clean up temporary working directories
clean:
	rm -f ./pinpoint-script*.pkg

##  pkg - Create a package using pkgbuild
pkg: setup clean
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} --ownership recommended ./${PKGTITLE}-${PKGVERSION}.pkg