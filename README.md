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

Currently most operations require you to pass the `--python` flag, since the
standalone installation’s host Python (`sys.executable`) is not capable of
creating a virtual environment.

You need to install a “proper” Python distribution (I selfishly recommend my
own [PythonUp] tool), and do something like:

```
pipx install --python=py [package-to-install]
```

[PythonUp]: https://github.com/uranusjr/pythonup-windows
