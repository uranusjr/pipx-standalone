# Build Script and Bucket to Publish pipx to Scoop

See respective documentation to get an idea what [pipx] and [Scoop] are.

[pipx]: https://pipxproject.github.io/pipx/
[Scoop]: https://scoop.sh/


## Usage

```
scoop bucket add pipx https://github.com/uranusjr/pipx-standalone.git
scoop install pipx-64  # Or pipx-32 if you’re running 32-bit.
```


## This is highly experiemental!

You need to install a “proper” Python distribution (I selfishly recommend my
own [PythonUp] tool). pipx is patched to use `py.exe` as default (instead of
`sys.executable` which won’t work).

[PythonUp]: https://github.com/uranusjr/pythonup-windows


## Release

Documentation for future self.

Update pipx version (and build number) in `main.py`.

```
py main.py --variant amd64
py main.py --variant win32
```

[Create a release](https://github.com/uranusjr/pipx-standalone/releases/new)
and upload the generated zip files.
