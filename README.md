# swarmanoid
Avengers, Assemble!!!

# Installation

Use nix package manager with `flakes` enabled to utilize the power of declerative configuration `flake.nix`

If you are not using `nixOS`:

1. First install the nix package manager from the link below:
(It should be as easy as pasting the command and following the script.)

```
https://nixos.org/download
```

2. Run the given script `enable-flakes-non-nixos.sh` with superuser permissions:

```
# With great power comes great responsibilities.
sudo ./enable-flakes-non-nixos.sh
```

3. Run `nix develop`. For the first time it will take some time to install `opencv`, because it should be compiled manually with the `enableGTK2` flag to displaying windows using the `opencv` library itself. The environment will be loaded instantly upon running `nix develop` the next time.

4. `./aruco.py` to run the program.

> Note: Since, the development is done in the nix environment you should enter the environment each time running `nix develop` if you exit or closed the terminal.

> using `flake.nix` to add the dependencies and environment variable is highly recommended.
