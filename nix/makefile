DEPENDENCIES=postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses

requirements.nix: ../requirements.txt requirements_override.nix
	pypi2nix -v -r ../requirements.txt -V python37 -E "$(DEPENDENCIES)"
