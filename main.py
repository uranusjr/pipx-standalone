import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.request
import zipfile


PIPX_VERSION = "0.16.3"

# Used to release manifest bug fixes without incrementing pipx version.
MANIFEST_BUILD_NUMBER = 0

PYTHON_EMBED_VERSION = "3.9.5"

PYTHON_EMBED_URL_TEMPLATE = (
    "https://www.python.org/ftp/python/{0}/python-{0}-embed-{1}.zip"
)

PYTHON_EMBED_URLS = {
    variant: PYTHON_EMBED_URL_TEMPLATE.format(PYTHON_EMBED_VERSION, variant)
    for variant in ["amd64", "win32"]
}


def retrieve_python(url: str, dl_dir: pathlib.Path, build_dir: pathlib.Path):
    archive = dl_dir.joinpath(url.rsplit("/", 1)[-1])
    if not archive.exists():
        urllib.request.urlretrieve(url, archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(build_dir)


def retrieve_pipx(build_dir: pathlib.Path):
    env = os.environ.copy()
    env.update({
        "PIP_REQUIRE_VIRTUALENV": "false",
        "PIP_DISABLE_PIP_VERSION_CHECK": "true",
        "PIP_NO_WARN_SCRIPT_LOCATION": "false",
    })
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            f"pipx=={PIPX_VERSION}",
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

    artifacts = []
    for variant, url in PYTHON_EMBED_URLS.items():
        dist_name = f"pipx-standalone-{variant}-{PIPX_VERSION}"
        if MANIFEST_BUILD_NUMBER:
            dist_name += f"+{MANIFEST_BUILD_NUMBER}"

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

        print(f"Downloading {url}")
        retrieve_python(url, ns.build, build_dir)

        # pip would emit output so we don't.
        retrieve_pipx(build_dir)

        # print(f"Patching {build_dir.joinpath('pipx')}")
        # patch_pipx(build_dir)

        print("Creating archive...", end=" ", flush=True)
        create_archive(build_dir, target)
        artifacts.append(target)
        print("Done")

    print("\nCreated:")
    for artifact in artifacts:
        print(f"    {artifact}")
    print()


if __name__ == "__main__":
    main()
