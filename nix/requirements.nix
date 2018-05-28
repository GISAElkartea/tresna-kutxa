# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -r ../requirements.txt -V 3.6 -E postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl
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

  commonBuildInputs = with pkgs; [ postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ];
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
      name = "Django-2.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/87/9f/4ec8b197d83666fddd2398842024c5341ee7d40bbec6aee9705d1ad22f13/Django-2.0.tar.gz"; sha256 = "9614851d4a7ff8cbd32b73c6076441f377c45a5bbff7e771798fb02c43c31f47"; };
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
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/b3/73/fc5c850f44af5889192dff783b7b0d8f3fe8d30b65c8e3f78f8f0265fecf/Markdown-2.6.11.tar.gz"; sha256 = "a856869c7ff079ad84a3e19cd87a64998350c2b94e9e08e44270faef33400f81"; };
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
      name = "Pillow-5.1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/89/b8/2f49bf71cbd0e9485bb36f72d438421b69b7356180695ae10bd4fd3066f5/Pillow-5.1.0.tar.gz"; sha256 = "cee9bc75bff455d317b6947081df0824a8f118de2786dc3d74a3503fd631f4ef"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://python-pillow.org";
        license = "License :: Other/Proprietary License";
        description = "Python Imaging Library (Fork)";
      };
    };



    "django-debug-toolbar" = python.mkDerivation {
      name = "django-debug-toolbar-1.9.1";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/50/95/e3d04d645f596b32320b88ade97571416d0520c083e4172f9fca808af62f/django-debug-toolbar-1.9.1.tar.gz"; sha256 = "d9ea75659f76d8f1e3eb8f390b47fc5bad0908d949c34a8a3c4c87978eb40a0f"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Django"
      self."sqlparse"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jazzband/django-debug-toolbar";
        license = licenses.bsdOriginal;
        description = "A configurable set of panels that display various debug information about the current request/response.";
      };
    };



    "django-filter" = python.mkDerivation {
      name = "django-filter-1.1.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/db/12/491d519f5bee93709083c726b020ff9f09b95f32de36ae9023fbc89a21e4/django-filter-1.1.0.tar.gz"; sha256 = "ec0ef1ba23ef95b1620f5d481334413700fb33f45cd76d56a63f4b0b1d76976a"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/carltongibson/django-filter/tree/master";
        license = licenses.bsdOriginal;
        description = "Django-filter is a reusable Django application for allowing users to filter querysets dynamically.";
      };
    };



    "django-localized-fields" = python.mkDerivation {
      name = "django-localized-fields-4.6a3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/06/c1/6a47997acfc5dd031653c4a4f70c8b5ad1c1bfa0d2c465a79a8b0e5d2523/django-localized-fields-4.6a3.tar.gz"; sha256 = "4ef6cb3b8d7b1274c0a9c1bd31a52a9c2eed80e308078a92deee8db7da7a24b0"; };
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
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/6a/99/6e73d10ec4d8f1e0419a15c16cc9a9fab932735a9ec5b139797689791524/django-postgres-extra-1.20.tar.gz"; sha256 = "2a88408476dcf5d5b0ff952572fd6a0187204be68d7afc269a9107fbe9633d0b"; };
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
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/70/e3/9372fcdca8e9c3205e7979528ccd1a14354a9a24d38efff11c1846ff8bf1/django-ranged-response-0.2.0.tar.gz"; sha256 = "f71fff352a37316b9bead717fc76e4ddd6c9b99c4680cdf4783b9755af1cf985"; };
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
      name = "django-simple-captcha-0.5.6";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/4d/46/44aff307e370e873ebb44dd8e9a1bcde10ddd1e55779361a5654d273d939/django-simple-captcha-0.5.6.zip"; sha256 = "d6fd36e8ba4215908f8698ae0ee40ed2591f7ce544f6eb1a2c84a84ea55e4b0b"; };
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
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/eb/9f/dd7b624de57eae649d4768b91aa27d617805ec0fbabbf3bc374c5c8cfd91/django-watson-1.5.2.tar.gz"; sha256 = "2697c8acf77fd8f0f957d4b71bd9f07f359bb3954a3516a339cac87b3c9f1c9f"; };
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
      name = "psycopg2-2.7.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/74/83/51580322ed0e82cba7ad8e0af590b8fb2cf11bd5aaa1ed872661bd36f462/psycopg2-2.7.4.tar.gz"; sha256 = "8bf51191d60f6987482ef0cfe8511bbf4877a5aa7f313d7b488b53189cf26209"; };
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
      name = "pytz-2018.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/10/76/52efda4ef98e7544321fd8d5d512e11739c1df18b0649551aeccfb1c8376/pytz-2018.4.tar.gz"; sha256 = "c06425302f2cf668f1bba7a0a03f3c1d34d4ebeef2c72003da308b3947c7f749"; };
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
      name = "six-1.11.0";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/16/d8/bc6316cf98419719bd59c91742194c111b6f2e85abac88e496adefaf7afe/six-1.11.0.tar.gz"; sha256 = "70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pypi.python.org/pypi/six/";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };



    "sqlparse" = python.mkDerivation {
      name = "sqlparse-0.2.4";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/79/3c/2ad76ba49f9e3d88d2b58e135b7821d93741856d1fe49970171f73529303/sqlparse-0.2.4.tar.gz"; sha256 = "ce028444cfab83be538752a2ffdb56bc417b7784ff35bb9a3062413717807dec"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/andialbrecht/sqlparse";
        license = licenses.bsdOriginal;
        description = "Non-validating SQL parser";
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