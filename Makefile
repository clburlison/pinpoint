# Makefile for pinpoint related tasks
# Variables below

INSTALL_PATH="/Library/Application Support/pinpoint"
PKGTITLE="pinpoint"
PKGVERSION=$(shell ./pinpoint.py --version)
PKGID=com.clburlison.pinpoint
PROJECT="pinpoint"

#################################################

##Help - Show this help menu
help: 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##  clean - Clean up temporary working directories
clean:
	rm -rf pkgroot
	rm -f ./pinpoint*.{dmg,pkg}

##  pkg - Create a package using pkgbuild
pkg: clean
	mkdir -p pkgroot/${INSTALL_PATH}/bin
	mkdir -p pkgroot/Library/LaunchDaemons
	cp ./pinpoint.py pkgroot/${INSTALL_PATH}/bin
	cp ./com.clburlison.pinpoint.plist pkgroot/Library/LaunchDaemons/
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} --ownership recommended ./${PKGTITLE}-${PKGVERSION}.pkg

##  dmg - Wrap the package inside a dmg
dmg: pkg
	rm -f ./${PROJECT}*.dmg
	rm -rf /tmp/${PROJECT}-build
	mkdir -p /tmp/${PROJECT}-build/
	cp ./README.md /tmp/${PROJECT}-build
	cp -R ./${PKGTITLE}-${PKGVERSION}.pkg /tmp/${PROJECT}-build
	hdiutil create -srcfolder /tmp/${PROJECT}-build -volname "${PROJECT}" -format UDZO -o ${PROJECT}-${PKGVERSION}.dmg
	rm -rf /tmp/${PROJECT}-build