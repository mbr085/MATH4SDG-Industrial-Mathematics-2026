{
  description = "Python and Jupyter development environment for MATH4SDG 2026";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python312;
          # Preload native libraries in Python only, not in GUI subprocesses.
          # PyPI wheels on NixOS can require libstdc++ and zlib without RPATHs.
          pythonRuntime = pkgs.writeTextDir "sitecustomize.py" ''
            import ctypes

            for library in (
                "${pkgs.stdenv.cc.cc.lib}/lib/libstdc++.so.6",
                "${pkgs.zlib}/lib/libz.so.1",
            ):
                ctypes.CDLL(library, mode=ctypes.RTLD_GLOBAL)
          '';
        in
        {
          default = pkgs.mkShell {
            packages = [
              python
              pkgs.uv
              pkgs.pkg-config
            ];

            # Keep uv on the Nix-provided interpreter.
            UV_PYTHON = "${python}/bin/python3.12";
            UV_PYTHON_DOWNLOADS = "never";
            UV_PYTHON_PREFERENCE = "only-system";

            # Only Python processes receive libstdc++ and zlib. The
            # sitecustomize module runs before compiled wheels are imported.
            # Crucially, do NOT export LD_LIBRARY_PATH: KDE and browsers
            # must continue using their own compatible runtime libraries.
            shellHook = ''
              export PYTHONPATH="${pythonRuntime}''${PYTHONPATH:+:$PYTHONPATH}"
            '';
          };
        });
    };
}
