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
        paho-mqtt
      ]);

    dependencies = with pkgs; [
      # Micropython Dependencies
      esptool
      screen
      adafruit-ampy
      mosquitto
    ];

    shellHook = ''
      alias run="python ./main.py"
      # mosquitto -c resources/mosquitto.conf &
      screen -S mqtt-session -dm mosquitto -c resources/mosquitto.conf
      alias show="screen -r mqtt-session"

      echo "Type 'show' to see the mosquitto logs and 'ctrl+a+d' to hide it"
      echo "Type 'run' and 'run -m' for detection and 'run -q' for mqtt"
    '';
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [pythonEnv] ++ dependencies;
      shellHook = shellHook;
    };
  };
}
