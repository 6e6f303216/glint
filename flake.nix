{
  description = "Glint application development and build";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        
        pythonEnv = pkgs.python3.withPackages (ps: [
          ps.pyqt6
          ps.chess
          ps.requests
        ]);
        
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.stockfish
            pkgs.pyinstaller
          ];
        };

        packages.default = pkgs.stdenv.mkDerivation {
          name = "glint";
          src = ./.;

          nativeBuildInputs = [
            pythonEnv
            pkgs.pyinstaller
            pkgs.upx
            pkgs.stockfish
          ];

          buildPhase = ''
            pyinstaller \
              --name glint \
              --console \
              --onefile \
              --noconfirm \
              --upx \
              main.py
          '';

          installPhase = ''
            mkdir -p $out/bin
            cp dist/glint $out/bin/
          '';
        };
      }
    );
}