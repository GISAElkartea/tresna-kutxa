# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -v -r ../requirements.txt -V python37 -E 'postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses libsass' -N SYSTEM_SASS=1
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
  };

  commonBuildInputs = with pkgs; [ postgresql pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl ncurses libsass ];
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
      name = "django-2.2.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0d/05/5de305261e0a6bcd5701e2bfb5237e76303fde36f1f7c5a40ff86480ab5a/Django-2.2.7.tar.gz";
        sha256 = "16040e1288c6c9f68c6da2fe75ebde83c0a158f6f5d54f4c5177b0c1478c5b86";
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
        self."pip"
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
      name = "django-sass-processor-0.7.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6d/38/4d607938386244bc755dafa37e5dac6a222f6c3f1985d77b80c3e3712321/django-sass-processor-0.7.4.tar.gz";
        sha256 = "c1b56e76ce2b57382d26328ecdc204d3f65412d5da35df8a6b7bce6e7f754882";
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
      name = "libsass-0.19.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/bb/46/1fcb3086f43ab1793fbd53966d092c1fb3dade8780ce15a96ad520bce4c6/libsass-0.19.4.tar.gz";
        sha256 = "8b5b6d1a7c4ea1d954e0982b04474cc076286493f6af2d0a13c2e950fbe0be95";
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
      name = "markdown-2.6.11";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b3/73/fc5c850f44af5889192dff783b7b0d8f3fe8d30b65c8e3f78f8f0265fecf/Markdown-2.6.11.tar.gz";
        sha256 = "108g80ryzykh8bj0i7jfp71510wrcixdi771lf2asyghgyf8cmm8";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."setuptools"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://Python-Markdown.github.io/";
        license = licenses.bsdOriginal;
        description = "Python implementation of Markdown.";
      };
    };

    "packaging" = python.mkDerivation {
      name = "packaging-19.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5a/2f/449ded84226d0e2fda8da9252e5ee7731bdf14cd338f622dfcd9934e0377/packaging-19.2.tar.gz";
        sha256 = "28b924174df7a2fa32c1953825ff29c61e2f5e082343165438812f00d3a7fc47";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pyparsing"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/packaging";
        license = licenses.asl20;
        description = "Core utilities for Python packages";
      };
    };

    "pillow" = python.mkDerivation {
      name = "pillow-6.2.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5b/bb/cdc8086db1f15d0664dd22a62c69613cdc00f1dd430b5b19df1bea83f2a3/Pillow-6.2.1.tar.gz";
        sha256 = "bf4e972a88f8841d8fdc6db1a75e0f8d763e66e3754b03006cbc3854d89f1cb1";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-pillow.org";
        license = "HPND";
        description = "Python Imaging Library (Fork)";
      };
    };

    "pip" = python.mkDerivation {
      name = "pip-19.3.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ce/ea/9b445176a65ae4ba22dce1d93e4b5fe182f953df71a145f557cffaffc1bf/pip-19.3.1.tar.gz";
        sha256 = "21207d76c1031e517668898a6b46a9fb1501c7a4710ef5dfd6a40ad9e6757ea7";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pip.pypa.io/";
        license = licenses.mit;
        description = "The PyPA recommended tool for installing Python packages.";
      };
    };

    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.8.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/84/d7/6a93c99b5ba4d4d22daa3928b983cec66df4536ca50b22ce5dcac65e4e71/psycopg2-2.8.4.tar.gz";
        sha256 = "f898e5cc0a662a9e12bde6f931263a1bbd350cfb18e1d5336a12927851825bb6";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.lgpl2;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };

    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.4.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/00/32/8076fa13e832bb4dcff379f18f228e5a53412be0631808b9ca2610c0f566/pyparsing-2.4.5.tar.gz";
        sha256 = "4ca62001be367f01bd3e92ecbb79070272a9d4964dce6a48a82ff0b8bc7e683a";
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
      name = "pytz-2019.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/82/c3/534ddba230bd4fbbd3b7a3d35f3341d014cca213f369a9940925e7e5f691/pytz-2019.3.tar.gz";
        sha256 = "b02c06db6cf09c12dd25137e563b31700d3b80fcc4ad23abb7a315f2789819be";
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

    "setuptools" = python.mkDerivation {
      name = "setuptools-41.6.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/11/0a/7f13ef5cd932a107cd4c0f3ebc9d831d9b78e1a0e8c98a098ca17b1d7d97/setuptools-41.6.0.zip";
        sha256 = "6afa61b391dcd16cb8890ec9f66cc4015a8a31a6e1c2b4e0c464514be1a3d722";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools";
        license = licenses.mit;
        description = "Easily download, build, install, upgrade, and uninstall Python packages";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.13.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/94/3e/edcf6fef41d89187df7e38e868b2dd2182677922b600e880baad7749c865/six-1.13.0.tar.gz";
        sha256 = "30f610279e8b2578cab6db20741130331735c781b56053c59c4076da27f06b66";
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
        license = licenses.gpl2Plus;
        description = "The uWSGI server";
      };
    };

    "wheel" = python.mkDerivation {
      name = "wheel-0.33.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/59/b0/11710a598e1e148fb7cbf9220fd2a0b82c98e94efbdecb299cb25e7f0b39/wheel-0.33.6.tar.gz";
        sha256 = "10c9da68765315ed98850f8e048347c3eb06dd81822dc2ab1d4fde9dc9702646";
};
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/wheel";
        license = licenses.mit;
        description = "A built-package format for Python.";
      };
    };
  };
  localOverridesFile = ./requirements_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
        (let src = pkgs.fetchFromGitHub { owner = "nix-community"; repo = "pypi2nix-overrides"; rev = "6220f85d58a4ecbba24dce363007096e1240618a"; sha256 = "00nr5cwpdl52z44w1hsxsaisvwx1vhfpgl3xj758mg0rq4ifirk4"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
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
