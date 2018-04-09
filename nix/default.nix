{ pkgs ? import <nixpkgs> {} }:

import ./requirements.nix { inherit pkgs; }
