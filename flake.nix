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

            # Deliberately do not override LD_LIBRARY_PATH globally:
            # KDE/xdg-open and other Nix-built GUI apps require their own
            # compatible C++ runtime libraries. If a Python wheel needs a
            # shared library, solve that separately rather than polluting
            # every process launched from this development shell.
          };
        });
    };
}
