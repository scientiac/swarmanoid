{
  description = "Swarmanoid Environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: let
    system = "x86_64-linux";

    pkgs = nixpkgs.legacyPackages.${system};

    helpme = pkgs.writeShellScriptBin "swar" ''

    case $1 in
	"run")
	    shift
	    python ./main.py "$@"
	    ;;
	"show")
	    screen -r mqtt-session
	    ;;
	"repl")
	    screen /dev/ttyUSB0 115200
	    ;;
	"push")
	    ampy -p /dev/ttyUSB0 put "$2"
	    ;;
	"switch")
	    ./etc/change-values.sh
	    ;;
	*)
            echo "
To run commands:
swar <command> <flags/files>

show   - to see the mosquitto logs
    press [ctrl+a+d] to hide

run    - to run the main script
    [-s or --simulate] to simulate and host feed of the arena

repl   - to enter the micropython repl
    press [ctrl+a+k] and hit y to exit

push   - to send it to the client
    eg: push main.py

switch - to switch values of wifi and broker address and push
   [auto detection won't work on darwin]           
            "
        ;;
esac
    '';


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
        # Simulation
        pygame
        flask
        # LSP
        python-lsp-server
        black
      ]);

    dependencies = with pkgs; [
      # Micropython Dependencies
      esptool
      screen
      adafruit-ampy
      mosquitto
      helpme
      # For the script
      networkmanager
      wirelesstools
      gnused
      iproute2
      unixtools.ifconfig
    ];

    shellHook = ''
            screen -S mqtt-session -dm mosquitto -c etc/mosquitto.conf
            echo "Type 'swar' to get help!"
    '';

  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [pythonEnv] ++ dependencies;
      shellHook = shellHook;
    };
  };
}
