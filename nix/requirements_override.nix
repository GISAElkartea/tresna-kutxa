{ pkgs, python }:

self: super: {
    "django-sass-processor" = python.overrideDerivation super."django-sass-processor" (old: {
    buildInputs = old.buildInputs ++ [ pkgs.glibcLocales ];
    preConfigure = ''
        export LANG=en_US.UTF-8
    '';
   });
}
