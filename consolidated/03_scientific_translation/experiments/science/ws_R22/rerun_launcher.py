#!/usr/bin/env python3
"""R22 launcher for re-running another division's multi-module scripts in isolated mode.
`python3 -I -B <script>` does not put the script's directory on sys.path (isolated mode), so sibling imports
(`from geomlib import ...`) fail.  This launcher adds exactly ONE directory -- the scratch copy -- and runs the script
as __main__.   Usage: python3 -I -B rerun_launcher.py <copy_dir> <script.py> [args...]"""
import os, runpy, sys
copy_dir, script = os.path.abspath(sys.argv[1]), sys.argv[2]
sys.path.insert(0, copy_dir)
sys.argv = [os.path.join(copy_dir, script)] + sys.argv[3:]
runpy.run_path(sys.argv[0], run_name="__main__")
