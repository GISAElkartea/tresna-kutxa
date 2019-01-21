# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -r ../requirements.txt -V 3 -E postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses
#

{ pkgs ? import <nixpkgs> {}
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python3;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            sed -i               -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"                  $out/${pkgs.python35.sitePackages}/pip/req/req_install.py
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreter = pythonPackages.buildPythonPackage {
        name = "python3-interpreter";
        buildInputs = [ makeWrapper ] ++ (builtins.attrValues pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter}               $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "               (builtins.attrValues pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -f $prog ]; then
                  ln -s $prog $out/bin/`basename $prog`
                fi
              done
            fi
          done
          for prog in "$out/bin/"*; do
            wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
          done
          pushd $out/bin
          ln -s ${pythonPackages.python.executable} python
          ln -s ${pythonPackages.python.executable}               python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };
    in {
      __old = pythonPackages;
      inherit interpreter;
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs //                                            { meta = drv.meta; });
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {

    "Django" = python.mkDerivation {
      name = "Django-2.1.5";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/5c/7f/4c750e09b246621e5e90fa08f93dec1b991f5c203b0ff615d62a891c8f41/Django-2.1.5.tar.gz"; sha256 = "d6393918da830530a9516bbbcbf7f1214c3d733738779f06b0f649f49cc698c3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."pytz"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.djangoproject.com/";
        license = licenses.bsdOriginal;
        description = "A high-level Python Web framework that encourages rapid development and clean, pragmatic design.";
      };
    };



    "Markdown" = python.mkDerivation {
      name = "Markdown-2.6.11";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/b3/73/fc5c850f44af5889192dff783b7b0d8f3fe8d30b65c8e3f78f8f0265fecf/Markdown-2.6.11.tar.gz"; sha256 = "a856869c7ff079ad84a3e19cd87a64998350c2b94e9e08e44270faef33400f81"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://Python-Markdown.github.io/";
        license = licenses.bsdOriginal;
        description = "Python implementation of Markdown.";
      };
    };



    "Pillow" = python.mkDerivation {
      name = "Pillow-5.3.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/1b/e1/1118d60e9946e4e77872b69c58bc2f28448ec02c99a2ce456cd1a272c5fd/Pillow-5.3.0.tar.gz"; sha256 = "2ea3517cd5779843de8a759c2349a3cd8d3893e03ab47053b66d5ec6f8bc4f93"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-pillow.org";
        license = "License :: Other/Proprietary License";
        description = "Python Imaging Library (Fork)";
      };
    };



    "django-appconf" = python.mkDerivation {
      name = "django-appconf-1.0.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/34/b9/d07195652ab494b026f7cb0341dd6e5f2e6e39be177abe05e2cec8bd46e4/django-appconf-1.0.2.tar.gz"; sha256 = "6a4d9aea683b4c224d97ab8ee11ad2d29a37072c0c6c509896dd9857466fb261"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://django-appconf.readthedocs.org/";
        license = licenses.bsdOriginal;
        description = "A helper class for handling configuration defaults of packaged apps gracefully.";
      };
    };



    "django-compressor" = python.mkDerivation {
      name = "django-compressor-2.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/82/76/1355459f90714517c52f264aa7245b52e59a273ec16e8f8d505fa6c342f8/django_compressor-2.2.tar.gz"; sha256 = "9616570e5b08e92fa9eadc7a1b1b49639cce07ef392fc27c74230ab08075b30f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."django-appconf"
      self."rcssmin"
      self."rjsmin"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://django-compressor.readthedocs.io/en/latest/";
        license = licenses.mit;
        description = "Compresses linked and inline JavaScript or CSS into single cached files.";
      };
    };



    "django-filter" = python.mkDerivation {
      name = "django-filter-2.0.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/6b/a4/b1ef813e7dd74ef193ae45849f592141cdfbd93bac206347ab5ded149335/django-filter-2.0.0.tar.gz"; sha256 = "6f4e4bc1a11151178520567b50320e5c32f8edb552139d93ea3e30613b886f56"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Django"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/carltongibson/django-filter/tree/master";
        license = licenses.bsdOriginal;
        description = "Django-filter is a reusable Django application for allowing users to filter querysets dynamically.";
      };
    };



    "django-localized-fields" = python.mkDerivation {
      name = "django-localized-fields-4.6a3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/06/c1/6a47997acfc5dd031653c4a4f70c8b5ad1c1bfa0d2c465a79a8b0e5d2523/django-localized-fields-4.6a3.tar.gz"; sha256 = "4ef6cb3b8d7b1274c0a9c1bd31a52a9c2eed80e308078a92deee8db7da7a24b0"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Django"
      self."django-postgres-extra"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/SectorLabs/django-localized-fields";
        license = licenses.mit;
        description = "Implementation of localized model fields using PostgreSQL HStore fields.";
      };
    };



    "django-markdownx" = python.mkDerivation {
      name = "django-markdownx-2.0.22";
      src = pkgs.fetchurl { url = "https://github.com/neutronX/django-markdownx/archive/bd06b48.zip"; sha256 = "dc4dfcdfd672b45afc63acc10172ecd1d8f2b2dbeb6f4965adc5a01aca1aef3d"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Django"
      self."Markdown"
      self."Pillow"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/neutronX/django-markdownx";
        license = licenses.bsdOriginal;
        description = "A comprehensive Markdown editor built for Django.";
      };
    };



    "django-postgres-extra" = python.mkDerivation {
      name = "django-postgres-extra-1.20";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/6a/99/6e73d10ec4d8f1e0419a15c16cc9a9fab932735a9ec5b139797689791524/django-postgres-extra-1.20.tar.gz"; sha256 = "2a88408476dcf5d5b0ff952572fd6a0187204be68d7afc269a9107fbe9633d0b"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/SectorLabs/django-postgres-extra";
        license = licenses.mit;
        description = "Bringing all of PostgreSQL's awesomeness to Django.";
      };
    };



    "django-ranged-response" = python.mkDerivation {
      name = "django-ranged-response-0.2.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/70/e3/9372fcdca8e9c3205e7979528ccd1a14354a9a24d38efff11c1846ff8bf1/django-ranged-response-0.2.0.tar.gz"; sha256 = "f71fff352a37316b9bead717fc76e4ddd6c9b99c4680cdf4783b9755af1cf985"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Django"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/wearespindle/django-ranged-fileresponse";
        license = licenses.mit;
        description = "Modified Django FileResponse that adds Content-Range headers.";
      };
    };



    "django-sass-processor" = python.mkDerivation {
      name = "django-sass-processor-0.7.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/93/2d/0f50d7414d59131e5365a869c1092996ad3c6b112b6409f5c80576cae101/django-sass-processor-0.7.2.tar.gz"; sha256 = "0381585a23c0f31a387cb53cf38f744e4d97d8ac3b9b19ec423dd6bfa714ecff"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."libsass"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jrief/django-sass-processor";
        license = licenses.mit;
        description = "SASS processor to compile SCSS files into *.css, while rendering, or offline.";
      };
    };



    "django-simple-captcha" = python.mkDerivation {
      name = "django-simple-captcha-0.5.9";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/d7/f4/ea95b04ed3abc7bf225716f17e35c5a185f6100db4d7541a46696ce40351/django-simple-captcha-0.5.9.zip"; sha256 = "0c30a14f02502119fd1a4d308dd5d2b899d0f4284825a396bbb010afd904754a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Django"
      self."Pillow"
      self."django-ranged-response"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mbi/django-simple-captcha";
        license = licenses.mit;
        description = "A very simple, yet powerful, Django captcha application";
      };
    };



    "libsass" = python.mkDerivation {
      name = "libsass-0.16.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/9d/00/cee3eae997e9d423f874a5d45a05e62965d0bea1c83c7aa8e8f9f8bd5c79/libsass-0.16.1.tar.gz"; sha256 = "5043f64d37254a6cfff8f1d2adcf13efecfda7e31ea09eb809269e117c8d8736"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://sass.github.io/libsass-python/";
        license = licenses.mit;
        description = "Sass for Python: A straightforward binding of libsass for Python.";
      };
    };



    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.7.6.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/c0/07/93573b97ed61b6fb907c8439bf58f09957564cf7c39612cef36c547e68c6/psycopg2-2.7.6.1.tar.gz"; sha256 = "27959abe64ca1fc6d8cd11a71a1f421d8287831a3262bd4cacd43bbf43cc3c82"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.lgpl2;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };



    "pytz" = python.mkDerivation {
      name = "pytz-2018.9";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/af/be/6c59e30e208a5f28da85751b93ec7b97e4612268bb054d0dff396e758a90/pytz-2018.9.tar.gz"; sha256 = "d5f05e487007e29e03409f9398d074e158d920d36eb82eaf66fb1136b0c5374c"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
      };
    };



    "rcssmin" = python.mkDerivation {
      name = "rcssmin-1.0.6";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/e2/5f/852be8aa80d1c24de9b030cdb6532bc7e7a1c8461554f6edbe14335ba890/rcssmin-1.0.6.tar.gz"; sha256 = "ca87b695d3d7864157773a61263e5abb96006e9ff0e021eff90cbe0e1ba18270"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://opensource.perlig.de/rcssmin/";
        license = "Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/";
        description = "CSS Minifier";
      };
    };



    "rjsmin" = python.mkDerivation {
      name = "rjsmin-1.0.12";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/10/9c/2c45f57d43258b05bf33cf8f6c8161ea5abf8b4776a5c59d12646727cd98/rjsmin-1.0.12.tar.gz"; sha256 = "dd9591aa73500b08b7db24367f8d32c6470021f39d5ab4e50c7c02e4401386f1"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://opensource.perlig.de/rjsmin/";
        license = "Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/";
        description = "Javascript Minifier";
      };
    };



    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz"; sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };



    "uWSGI" = python.mkDerivation {
      name = "uWSGI-2.0.17.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/a2/c9/a2d5737f63cd9df4317a4acc15d1ddf4952e28398601d8d7d706c16381e0/uwsgi-2.0.17.1.tar.gz"; sha256 = "d2318235c74665a60021a4fc7770e9c2756f9fc07de7b8c22805efe85b5ab277"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://uwsgi-docs.readthedocs.io/en/latest/";
        license = licenses.gpl2Plus;
        description = "The uWSGI server";
      };
    };

  };
  localOverridesFile = ./requirements_override.nix;
  overrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [

  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [overrides] else [] ) ++ commonOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )