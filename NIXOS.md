# NixOS maintainer setup

These are optional development notes for maintainers using NixOS. **Students on Windows and macOS should use [INSTALL.md](INSTALL.md).**

From the repository root:

```sh
nix develop
uv sync --locked
uv run jupyter lab
```

The checked-in `flake.nix` supplies Python 3.12 and uv. The flake pins its Nixpkgs input in `flake.lock`, while `uv.lock` pins the Python dependencies.

For a Fish shell with direnv/nix-direnv already configured, `direnv allow` can load the development shell automatically when entering the repository. The `.envrc` contains `use flake`.

The Nix environment configures uv to use the Python interpreter supplied by the flake, rather than downloading another interpreter. The repository also includes a narrowly scoped Python startup helper for required native libraries. No extra installation of the workshop's own `tools/` modules is necessary: the notebooks use `notebooks/bootstrap.py` where appropriate.

To run offline checks:

```sh
uv run python -m unittest discover -s tests -v
```

For the general student workflow, see [INSTALL.md](INSTALL.md).
