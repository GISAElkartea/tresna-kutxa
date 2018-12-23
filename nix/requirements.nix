# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -r ../requirements.txt -V 3.6 -E postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses
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
    python = pkgs.python36;
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
        name = "python36-interpreter";
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
      name = "Django-2.1.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/83/f7/4939b60c4127d5f49ccb570e34f4c59ecc222949220234a88e4f363f1456/Django-2.1.4.tar.gz"; sha256 = "068d51054083d06ceb32ce02b7203f1854256047a0d58682677dd4f81bceabd7"; };
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
      name = "Markdown-3.0.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/3c/52/7bae9e99a7a4be6af4a713fe9b692777e6468d28991c54c273dfb6ec9fb2/Markdown-3.0.1.tar.gz"; sha256 = "d02e0f9b04c500cde6637c11ad7c72671f359b87b9fe924b2383649d8841db7c"; };
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



    "django-watson" = python.mkDerivation {
      name = "django-watson-1.5.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/eb/9f/dd7b624de57eae649d4768b91aa27d617805ec0fbabbf3bc374c5c8cfd91/django-watson-1.5.2.tar.gz"; sha256 = "2697c8acf77fd8f0f957d4b71bd9f07f359bb3954a3516a339cac87b3c9f1c9f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/etianen/django-watson";
        license = licenses.bsdOriginal;
        description = "Full-text multi-table search application for Django. Easy to install and use, with good performance.";
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
      name = "pytz-2018.7";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/cd/71/ae99fc3df1b1c5267d37ef2c51b7d79c44ba8a5e37b48e3ca93b4d74d98b/pytz-2018.7.tar.gz"; sha256 = "31cb35c89bd7d333cd32c5f278fca91b523b0834369e757f4c5641ea252236ca"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
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