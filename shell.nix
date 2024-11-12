{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python311Packages.networkx
    pkgs.python311Packages.graphviz
    pkgs.python311Packages.tqdm
    pkgs.python311Packages.numpy
  ];

  shellHook = ''
    echo "Welcome to your Python development environment!"
    echo "Python version: $(python --version)"
  '';
}
