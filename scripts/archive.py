#!/usr/bin/env python3

import os
import sys
import shutil
import hashlib
import argparse
from glob import glob
from pathlib import Path

try:
    import filetype
except ModuleNotFoundError:
    print("===> attempt to install `filetype` using pip")
    import pip

    pip.main(["install", "filetype", "--user"])
    del pip

    import filetype


def get_downloads_path():
    if os.name == "nt":
        import ctypes
        from ctypes import windll, wintypes
        from uuid import UUID

        # ctypes GUID copied from MSDN sample code
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD), ("Data2", wintypes.WORD), ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
            ]

            def __init__(self, uuidstr):
                uuid = UUID(uuidstr)
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, \
                    self.Data4[0], self.Data4[1], rest = uuid.fields
                for i in range(2, 8):
                    self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff

        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p)
        ]

        def _get_known_folder_path(uuidstr):
            pathptr = ctypes.c_wchar_p()
            guid = GUID(uuidstr)
            if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
                raise ctypes.WinError()
            return pathptr.value

        FOLDERID_Download = "{374DE290-123F-4565-9164-39C4925E467B}"

        return _get_known_folder_path(FOLDERID_Download)
    else:
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")


def parse_args():
    dowloads_path = Path(get_downloads_path())
    default_dest_path = (Path(__file__).parent.parent / "archived_emoticons").absolute()

    parser = argparse.ArgumentParser(
        description="Archive saved Wechat emoticons from Downloads folder",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-s",
        "--source",
        type=Path,
        default=dowloads_path,
        help="path to the Downloads folder of this computer\n"
        "default: {}".format(dowloads_path),
    )
    parser.add_argument(
        "-d",
        "--dest",
        type=Path,
        default=default_dest_path,
        help="path to the folder that stores archived emoticons\n"
        "default: {}".format(default_dest_path),
    )
    return parser.parse_args()


def md5sum(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def load_archived_hashes(path: Path) -> set:
    results = set()
    for filename in path.iterdir():
        results.add(filename.name.rpartition(".")[0])

    return results


def main(args):
    if not args.dest.is_dir():
        print("Creating", args.dest)
        args.dest.mkdir(parents=True, exist_ok=True)

    archived_hashes = load_archived_hashes(args.dest)

    source_dir = args.source / "wx_emoticons"
    for filename in source_dir.rglob("**/*"):
        if filename.is_dir():
            continue

        md5hash = md5sum(filename)
        if md5hash in archived_hashes:
            print("Duplicated. Skipped", filename)
            continue

        fileext = filetype.guess_extension(str(filename))

        if fileext is None:
            print("Broken. Skipped", filename)
            continue

        archived_hashes.add(md5hash)
        dest_filename = args.dest / "{}.{}".format(md5hash, fileext)
        print("Storing {} to {}".format(filename, dest_filename))

        shutil.copy2(filename, dest_filename)


if __name__ == "__main__":
    main(parse_args())