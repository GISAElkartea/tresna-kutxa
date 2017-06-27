{ pkgs, python }:

self: super: {

  "django-localized-fields" = python.overrideDerivation super."django-localized-fields" (old: {
    buildInputs = old.buildInputs ++ [ pkgs.glibcLocales ];
    preConfigure = ''
        export LANG=en_US.UTF-8
    '';
  });
}
