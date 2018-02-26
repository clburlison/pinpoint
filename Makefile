# Makefile for pinpoint related tasks

PKGTITLE="pinpoint"
PKGVERSION:=$(shell ./pkgroot/Library/Application\ Support/pinpoint/bin/pinpoint --version)
PKGID=com.clburlison.pinpoint
PROJECT="pinpoint"
PB_EXTRA_ARGS+= --sign "Developer ID Installer: Clayton Burlison"

#################################################

-include config.mk

##Help - Show this help menu
help: 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##  clean - Clean up temporary working directories
clean:
	rm -f ./pinpoint*.{dmg,pkg}
	rm -f ./pkgroot/Library/Application\ Support/pinpoint/bin/FoundationPlist/*.pyc

##  pkg - Create a package using pkgbuild
pkg: clean
	# pkgbuild --root pkgroot --scripts scripts --identifier ${PKGID} ${PB_EXTRA_ARGS} --version ${PKGVERSION} --ownership recommended ./${PKGTITLE}-${PKGVERSION}.pkg
	./build.py ${PKGVERSION} ${PKGID} ${PKGTITLE}


##  dmg - Wrap the package inside a dmg
dmg: pkg
	rm -f ./${PROJECT}*.dmg
	rm -rf /tmp/${PROJECT}-build
	mkdir -p /tmp/${PROJECT}-build/
	cp ./README.md /tmp/${PROJECT}-build
	cp -R ./${PKGTITLE}-${PKGVERSION}.pkg /tmp/${PROJECT}-build
	hdiutil create -srcfolder /tmp/${PROJECT}-build -volname "${PROJECT}" -format UDZO -o ${PROJECT}-${PKGVERSION}.dmg
	rm -rf /tmp/${PROJECT}-build

## changelog - Update the changelog file (repo maintainer task)
changelog:
	docker run -it --rm -v "$(shell pwd)":/usr/local/src/your-app \
	clburlison/github-changelog-generator \
	-u clburlison -p pinpoint \
	-t ${CHANGELOG_GITHUB_TOKEN}
	git add "CHANGELOG.md"
	git commit -m "chore: Update changelog"
