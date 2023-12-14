{
  description = "Swarmanoid Environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    python = let
      packageOverrides = self: super: {
        opencv4 = super.opencv4.override {
          enableGtk2 = true;
          gtk2 = pkgs.gnome2.gtk;
        };
      };
    in
      pkgs.python3.override {
        inherit packageOverrides;
        self = python;
      };

    pythonEnv = python.withPackages (ps:
      with ps; [
        opencv4
        numpy
        networkx
      ]);
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [pythonEnv];
    };
  };
}
