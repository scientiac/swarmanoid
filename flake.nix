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
      # For the script
      networkmanager
      wirelesstools
      gnused
      iproute2
      unixtools.ifconfig
    ];

    shellHook = ''
            alias run="python ./main.py"
            screen -S mqtt-session -dm mosquitto -c etc/mosquitto.conf
            alias show="screen -r mqtt-session"
            alias repl="screen /dev/ttyUSB0 115200"
            alias push="ampy -p /dev/ttyUSB0 put"
            alias switch='./etc/change-values.sh'
            echo "Type 'help' to get help!"

      function help(){
            echo "
      show   - to see the mosquitto logs
                press [ctrl+a+d] to hide

      run    - to run the main script
                [-m or --multiple] to detect multiple kind of markers
                [-q or --mqtt]     to run a test mqtt python server

      repl   - to enter the micropython repl
                press [ctrl+a+k] and hit y to exit

      push   - to send it to the client
                eg: push main.py

      switch - to switch values of wifi and broker address and push
            "
      }
    '';
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [pythonEnv] ++ dependencies;
      shellHook = shellHook;
    };
  };
}
