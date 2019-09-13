# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -v -r ../requirements.txt -V python37 -E 'postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses'
#

{ pkgs ? import <nixpkgs> {},
  overrides ? ({ pkgs, python }: self: super: {})
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python37;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = (if builtins.hasAttr "patchPhase" old then old.patchPhase else "") + ''
            if [ -e $out/${pkgs.python37.sitePackages}/pip/req/req_install.py ]; then
              sed -i \
                -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"  \
                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"  \
                $out/${pkgs.python37.sitePackages}/pip/req/req_install.py
            fi
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python37-interpreter";
        buildInputs = [ makeWrapper ] ++ (selectPkgsFn pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter} \
              $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "
              (selectPkgsFn pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -x "$prog" ] && [ -f "$prog" ]; then
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
          ln -s ${pythonPackages.python.executable} \
              python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };

      interpreter = interpreterWithPackages builtins.attrValues;
    in {
      __old = pythonPackages;
      inherit interpreter;
      inherit interpreterWithPackages;
      mkDerivation = args: pythonPackages.buildPythonPackage (args // {
        nativeBuildInputs = (args.nativeBuildInputs or []) ++ args.buildInputs;
      });
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (
          drv.drvAttrs // f drv.drvAttrs // { meta = drv.meta; }
        );
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {
    "attrs" = python.mkDerivation {
      name = "attrs-19.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cc/d9/931a24cc5394f19383fbbe3e1147a0291276afa43a0dc3ed0d6cd9fda813/attrs-19.1.0.tar.gz";
        sha256 = "f0b870f674851ecbfbbbd364d6b5cbdff9dcedbc7f3f5e18a6891057f21fe399";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };

    "deprecation" = python.mkDerivation {
      name = "deprecation-2.0.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/cd/94/8d9d6303f5ddcbf40959fc2b287479bd9a201ea9483373d9b0882ae7c3ad/deprecation-2.0.7.tar.gz";
        sha256 = "c0392f676a6146f0238db5744d73e786a43510d54033f80994ef2f4c9df192ed";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."packaging"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://deprecation.readthedocs.io/";
        license = licenses.asl20;
        description = "A library to handle automated deprecations";
      };
    };

    "django" = python.mkDerivation {
      name = "django-2.2.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/1d/06/79ddea0bfd4e7cd1f9fa4700c8e524820a5263c6fd8bb91db14f1812c17d/Django-2.2.5.tar.gz";
        sha256 = "deb70aa038e59b58593673b15e9a711d1e5ccd941b5973b30750d5d026abfd56";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pytz"
        self."sqlparse"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.djangoproject.com/";
        license = licenses.bsdOriginal;
        description = "A high-level Python Web framework that encourages rapid development and clean, pragmatic design.";
      };
    };

    "django-appconf" = python.mkDerivation {
      name = "django-appconf-1.0.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/8e/9e/0cf10dc64e69f553dd1f8d54b8c55c31fb632d60ddcaeab3f21c472005ca/django-appconf-1.0.3.tar.gz";
        sha256 = "35f13ca4d567f132b960e2cd4c832c2d03cb6543452d34e29b7ba10371ba80e3";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."django"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://django-appconf.readthedocs.io/";
        license = licenses.bsdOriginal;
        description = "A helper class for handling configuration defaults of packaged apps gracefully.";
      };
    };

    "django-compressor" = python.mkDerivation {
      name = "django-compressor-2.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/73/ba/e14cc0a8ebecb043175abee1dcab15b2612952f91793ddfdfeefd0892a2f/django_compressor-2.3.tar.gz";
        sha256 = "47c86347f75c64954a06afbbfc820a750619e10c23a49272b865020a407b7edd";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
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
      name = "django-filter-2.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/dc/75/af3f0c2682d2603617ee3061b36395a64fb9d70c327bb759de43e643e5b3/django-filter-2.2.0.tar.gz";
        sha256 = "c3deb57f0dd7ff94d7dce52a047516822013e2b441bed472b722a317658cfd14";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."django"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/carltongibson/django-filter/tree/master";
        license = licenses.bsdOriginal;
        description = "Django-filter is a reusable Django application for allowing users to filter querysets dynamically.";
      };
    };

    "django-localized-fields" = python.mkDerivation {
      name = "django-localized-fields-5.4";
      src = pkgs.fetchurl {
        url = "https://github.com/umazalakain/django-localized-fields/archive/bump-deprecation.zip";
        sha256 = "181bscj4zkl1mf78gmlmqcfw7my6hyx0jf5xis5vq9pyjbb5lbdl";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."deprecation"
        self."django"
        self."django-postgres-extra"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/SectorLabs/django-localized-fields";
        license = licenses.mit;
        description = "Implementation of localized model fields using PostgreSQL HStore fields.";
      };
    };

    "django-markdownx" = python.mkDerivation {
      name = "django-markdownx-2.0.28";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ca/fd/26af60865205ec37e1f62a2fabb6f69177268c8df047c4896f288a30fad4/django-markdownx-2.0.28.tar.gz";
        sha256 = "d6e706c0b1329b23d6dcaa8754e5921fa2531711dc5afeec4ed3c73a8cb6a178";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."django"
        self."markdown"
        self."pillow"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/neutronX/django-markdownx";
        license = licenses.bsdOriginal;
        description = "A comprehensive Markdown editor built for Django.";
      };
    };

    "django-postgres-extra" = python.mkDerivation {
      name = "django-postgres-extra-1.22";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/74/0e/78f0524822937b2f8055246a4cbba55753d8bef6a6d3289fd51bd9753952/django-postgres-extra-1.22.tar.gz";
        sha256 = "bb784822782c017300f2df68e24c1198fc0e4bd2b53c8e36251034d76730c447";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/SectorLabs/django-postgres-extra";
        license = licenses.mit;
        description = "Bringing all of PostgreSQL's awesomeness to Django.";
      };
    };

    "django-ranged-response" = python.mkDerivation {
      name = "django-ranged-response-0.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/70/e3/9372fcdca8e9c3205e7979528ccd1a14354a9a24d38efff11c1846ff8bf1/django-ranged-response-0.2.0.tar.gz";
        sha256 = "f71fff352a37316b9bead717fc76e4ddd6c9b99c4680cdf4783b9755af1cf985";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."django"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/wearespindle/django-ranged-fileresponse";
        license = licenses.mit;
        description = "Modified Django FileResponse that adds Content-Range headers.";
      };
    };

    "django-sass-processor" = python.mkDerivation {
      name = "django-sass-processor-0.7.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b7/ec/ba3dbb86590b6a9e140008da5aa1bfcbb0401ef49bf41ca02dff9c36a272/django-sass-processor-0.7.3.tar.gz";
        sha256 = "5ba3568e53caf1d59573afa75d71e42c23bddbd5b48cbea831816cd72ed242f9";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jrief/django-sass-processor";
        license = licenses.mit;
        description = "SASS processor to compile SCSS files into *.css, while rendering, or offline.";
      };
    };

    "django-simple-captcha" = python.mkDerivation {
      name = "django-simple-captcha-0.5.12";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/1d/84/82da15830a77ce3e667fc834e2e451864c24c78def86fa09caa934f17df5/django-simple-captcha-0.5.12.zip";
        sha256 = "fc25f0425e282aa82d2a65013049a8dc7c0682f8e05d32681c39a0c55ed322bd";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."django"
        self."django-ranged-response"
        self."pillow"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mbi/django-simple-captcha";
        license = licenses.mit;
        description = "A very simple, yet powerful, Django captcha application";
      };
    };

    "libsass" = python.mkDerivation {
      name = "libsass-0.19.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bb/25/56fbd361b36b449457f19beaf616abf8cdfb8e037ea8f3f8300b7c2950a8/libsass-0.19.2.tar.gz";
        sha256 = "cb50f385117535f7671ac7ff3144c1ef0b8e088778c58d269ce6f31b87bfad72";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://sass.github.io/libsass-python/";
        license = licenses.mit;
        description = "Sass for Python: A straightforward binding of libsass for Python.";
      };
    };

    "markdown" = python.mkDerivation {
      name = "markdown-3.1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ac/df/0ae25a9fd5bb528fe3c65af7143708160aa3b47970d5272003a1ad5c03c6/Markdown-3.1.1.tar.gz";
        sha256 = "2e50876bcdd74517e7b71f3e7a76102050edec255b3983403f1a63e7c8a41e7a";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://Python-Markdown.github.io/";
        license = licenses.bsdOriginal;
        description = "Python implementation of Markdown.";
      };
    };

    "packaging" = python.mkDerivation {
      name = "packaging-19.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/8b/3a/5bfe64c319be5775ed7ea3bc1a8e5667e0d57a740cc0498ce03e032eaf93/packaging-19.1.tar.gz";
        sha256 = "c491ca87294da7cc01902edbe30a5bc6c4c28172b5138ab4e4aa1b9d7bfaeafe";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."attrs"
        self."pyparsing"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/packaging";
        license = licenses.bsdOriginal;
        description = "Core utilities for Python packages";
      };
    };

    "pillow" = python.mkDerivation {
      name = "pillow-6.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/51/fe/18125dc680720e4c3086dd3f5f95d80057c41ab98326877fc7d3ff6d0ee5/Pillow-6.1.0.tar.gz";
        sha256 = "0804f77cb1e9b6dbd37601cee11283bba39a8d44b9ddb053400c58e0c0d7d9de";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-pillow.org";
        license = "UNKNOWN";
        description = "Python Imaging Library (Fork)";
      };
    };

    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.8.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5c/1c/6997288da181277a0c29bc39a5f9143ff20b8c99f2a7d059cfb55163e165/psycopg2-2.8.3.tar.gz";
        sha256 = "897a6e838319b4bf648a574afb6cabcb17d0488f8c7195100d48d872419f4457";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.zpl21;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };

    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.4.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7e/24/eaa8d7003aee23eda270099eeec754d7bf4399f75c6a011ef948304f66a2/pyparsing-2.4.2.tar.gz";
        sha256 = "6f98a7b9397e206d78cc01df10131398f1c8b8510a2f4d97d9abd82e1aacdd80";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pyparsing/pyparsing/";
        license = licenses.mit;
        description = "Python parsing module";
      };
    };

    "pytz" = python.mkDerivation {
      name = "pytz-2019.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/27/c0/fbd352ca76050952a03db776d241959d5a2ee1abddfeb9e2a53fdb489be4/pytz-2019.2.tar.gz";
        sha256 = "26c0b32e437e54a18161324a2fca3c4b9846b74a8dccddd843113109e1116b32";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
      };
    };

    "rcssmin" = python.mkDerivation {
      name = "rcssmin-1.0.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e2/5f/852be8aa80d1c24de9b030cdb6532bc7e7a1c8461554f6edbe14335ba890/rcssmin-1.0.6.tar.gz";
        sha256 = "ca87b695d3d7864157773a61263e5abb96006e9ff0e021eff90cbe0e1ba18270";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
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
      name = "rjsmin-1.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a2/ba/0fa30f7ec949714b8397e80ee2057d1a7e77b3a9f1b94c1ece93586cf34f/rjsmin-1.1.0.tar.gz";
        sha256 = "b15dc75c71f65d9493a8c7fa233fdcec823e3f1b88ad84a843ffef49b338ac32";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://opensource.perlig.de/rjsmin/";
        license = licenses.asl20;
        description = "Javascript Minifier";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz";
        sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "sqlparse" = python.mkDerivation {
      name = "sqlparse-0.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/63/c8/229dfd2d18663b375975d953e2bdc06d0eed714f93dcb7732f39e349c438/sqlparse-0.3.0.tar.gz";
        sha256 = "7c3dca29c022744e95b547e867cee89f4fce4373f3549ccd8797d8eb52cdb873";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/andialbrecht/sqlparse";
        license = licenses.bsdOriginal;
        description = "Non-validating SQL parser";
      };
    };

    "uwsgi" = python.mkDerivation {
      name = "uwsgi-2.0.18";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e7/1e/3dcca007f974fe4eb369bf1b8629d5e342bb3055e2001b2e5340aaefae7a/uwsgi-2.0.18.tar.gz";
        sha256 = "4972ac538800fb2d421027f49b4a1869b66048839507ccf0aa2fda792d99f583";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://uwsgi-docs.readthedocs.io/en/latest/";
        license = "GPLv2+";
        description = "The uWSGI server";
      };
    };
  };
  localOverridesFile = ./requirements_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
    
  ];
  paramOverrides = [
    (overrides { inherit pkgs python; })
  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [localOverrides] else [] ) ++ commonOverrides ++ paramOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )