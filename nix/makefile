DEPENDENCIES=postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses

requirements.nix: ../requirements.txt
	pypi2nix -r ../requirements.txt -V 3 -E "$(DEPENDENCIES)"
