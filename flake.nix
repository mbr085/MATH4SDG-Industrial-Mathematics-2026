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
          # Keep Quarto and all of its binary dependencies at the versions in
          # the official upstream release bundle. In particular, do not use
          # pkgs.quarto: nixpkgs replaces Quarto's bundled Pandoc and other
          # tools, which can produce an internally mismatched installation.
          quartoVersion = "1.10.18";

          quartoPlatform =
            if pkgs.stdenv.hostPlatform.system == "x86_64-linux" then
              {
                archive = "linux-amd64";
                toolArch = "x86_64";
                hash = "sha256-r60HG1vSLALy0wBpV0MYnTZQ4FN6Uwc+ZUtjDP8rDHM=";
              }
            else if pkgs.stdenv.hostPlatform.system == "aarch64-linux" then
              {
                archive = "linux-arm64";
                toolArch = "aarch64";
                hash = "sha256-9qB99o4lMwtd809l099mvKYFrM47gwxZOljpGITUz2w=";
              }
            else
              throw "Unsupported system for the pinned Quarto bundle: ${pkgs.stdenv.hostPlatform.system}";

          quartoUpstream = pkgs.stdenv.mkDerivation {
            pname = "quarto-upstream";
            version = quartoVersion;

            src = pkgs.fetchurl {
              url = "https://github.com/quarto-dev/quarto-cli/releases/download/v${quartoVersion}/quarto-${quartoVersion}-${quartoPlatform.archive}.tar.gz";
              inherit (quartoPlatform) hash;
            };

            sourceRoot = "quarto-${quartoVersion}";

            nativeBuildInputs = [ pkgs.makeWrapper pkgs.autoPatchelfHook ];

            buildInputs = [ pkgs.bashNonInteractive pkgs.stdenv.cc.cc.libgcc ];

            dontConfigure = true;
            dontBuild = true;
            dontStrip = true;

            installPhase = ''
              runHook preInstall

              mkdir -p "$out"
              cp -R bin share "$out/"

              # Make the bundled Pandoc directly available without replacing
              # the copy Quarto itself selects from bin/tools.
              ln -s "$out/bin/tools/${quartoPlatform.toolArch}/pandoc" "$out/bin/pandoc"

              # Quarto's launcher uses a few ordinary Unix utilities.
              wrapProgram "$out/bin/quarto" \
                --suffix PATH : ${
                  pkgs.lib.makeBinPath [
                    pkgs.coreutils
                    pkgs.which
                  ]
                }

              runHook postInstall
            '';

            meta = {
              description = "Quarto ${quartoVersion} with its upstream-bundled tools";
              homepage = "https://quarto.org/";
              license = pkgs.lib.licenses.mit;
              mainProgram = "quarto";
              platforms = systems;
              sourceProvenance = with pkgs.lib.sourceTypes; [
                binaryNativeCode
                binaryBytecode
              ];
            };
          };
        in
        {
          default = pkgs.mkShell {
            packages = [
              python
              pkgs.uv
              quartoUpstream
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
