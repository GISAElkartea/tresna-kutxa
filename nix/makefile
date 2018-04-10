DEPENDENCIES=postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl

requirements.nix: ../requirements.txt
	pypi2nix -r ../requirements.txt -V 3.6 -E "$(DEPENDENCIES)"
