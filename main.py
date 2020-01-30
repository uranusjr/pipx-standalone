import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.request
import zipfile


PYTHON_EMBED_URL = (
    "https://www.python.org/ftp/python/3.8.1/python-3.8.1-embed-amd64.zip"
)

PIPX_VERSION = "0.15.1.3"

BUILD_VERSION = None


def retrieve_python(dl_dir: pathlib.Path, build_dir: pathlib.Path):
    archive = dl_dir.joinpath(PYTHON_EMBED_URL.rsplit("/", 1)[-1])
    if not archive.exists():
        urllib.request.urlretrieve(PYTHON_EMBED_URL, archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(build_dir)


def retrieve_pipx(build_dir: pathlib.Path):
    env = os.environ.copy()
    env.update({
        "PIP_REQUIRE_VIRTUALENV": "false",
        "PIP_DISABLE_PIP_VERSION_CHECK": "true",
    })
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            f"pipx=={PIPX_VERSION}",
            "setuptools",  # TODO: Remove this for pipx>0.15.1.3.
            "--target",
            os.fspath(build_dir),
        ],
        env=env,
        check=True,
    )


def create_archive(source: pathlib.Path, target: pathlib.Path):
    with zipfile.ZipFile(target, "w") as zf:
        for dirpath, _, filenames in os.walk(source):
            # Don't need to package dist info.
            if os.path.splitext(dirpath)[-1] == ".dist-info":
                continue
            # Do not package entry points. They will be broken due
            # to we installing to a different location anyway.
            if dirpath == os.path.join(source, "bin"):
                continue
            for fn in filenames:
                absname = os.path.join(dirpath, fn)
                relname = os.path.relpath(absname, source)
                zf.write(absname, relname)
    return target


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().with_name("build"),
    )
    parser.add_argument(
        "--dist",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().with_name("dist"),
    )
    ns = parser.parse_args(argv)

    if BUILD_VERSION:
        dist_name = f"pipx-standalone-amd64-{PIPX_VERSION}-{BUILD_VERSION}"
    else:
        dist_name = f"pipx-standalone-amd64-{PIPX_VERSION}"

    build_dir = ns.build.joinpath(dist_name)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    dist_dir = ns.dist
    dist_dir.mkdir(parents=True, exist_ok=True)

    print(f"Building into: {build_dir}")

    target = dist_dir.joinpath(f"{build_dir.name}.zip")
    if target.exists():
        raise FileExistsError(target)

    retrieve_python(ns.build, build_dir)
    retrieve_pipx(build_dir)
    create_archive(build_dir, target)

    print(f"Created: {target}")


if __name__ == "__main__":
    main()
