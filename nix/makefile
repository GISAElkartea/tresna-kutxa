DEPENDENCIES=postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses

requirements.nix: ../requirements.txt requirements_override.nix
	nix run -f https://github.com/nix-community/pypi2nix/archive/master.tar.gz --command pypi2nix -v -r ../requirements.txt -V python37 -E "$(DEPENDENCIES)"
