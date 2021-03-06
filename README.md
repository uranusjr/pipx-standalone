# Build Script and Bucket to Publish pipx to Scoop

See respective documentation to get an idea what [pipx] and [Scoop] are.

[pipx]: https://pipxproject.github.io/pipx/
[Scoop]: https://scoop.sh/


## Usage

```bash
scoop bucket add pipx https://github.com/uranusjr/pipx-standalone.git
scoop install pipx

# Optional: Set environment variables where you want to put pipx stuff.
# More: https://pipxproject.github.io/pipx/installation/

pipx ensurepath  # Adds PIPX_BIN_DIR to PATH to expose executables as commands.
```


## This is highly experiemental!

You need to install a “proper” Python distribution. I selfishly recommend my
own [PythonUp] tool, but any installation is fine, including from
[installers from python.org](https://www.python.org/downloads/),
[Windows Store](https://www.microsoft.com/p/python-38/9mssztt1n39l),
or Scoop (`scoop install python`).

[PythonUp]: https://github.com/uranusjr/pythonup-windows


## Release

Documentation for future self.

Update `PIPX_VERSION` or `MANIFEST_BUILD_NUMBER` in `main.py`.

(Optional: Update `PYTHON_EMBED_VERSION`.)

Run `py main.py` to generate zip files.

[Create a release](https://github.com/uranusjr/pipx-standalone/releases/new)
and upload the generated zip files.

Update version and URL in `bucket/*.json`.

Push to master.
