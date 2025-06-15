{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pyqt6
    pkgs.python3Packages.chess
    pkgs.python3Packages.requests
    pkgs.stockfish

    pkgs.python3Packages.pyinstaller
  ];
}
