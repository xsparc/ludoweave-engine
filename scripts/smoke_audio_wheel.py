"""Verify optional audio wiring in an isolated wheel install, without hardware."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from collections.abc import Sequence
from pathlib import Path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path)
    args = parser.parse_args(argv)
    dist = Path(args.dist).resolve()
    wheels = sorted(dist.glob("ludoweave-*.whl"))
    if len(wheels) != 1:
        parser.error("dist must contain exactly one LudoWeave wheel")
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required")
    probe = textwrap.dedent(r"""
        import sys
        from unittest.mock import patch
        from ludoweave.audio import AudioClipDescriptor
        from ludoweave.audio.sounddevice import BlockingAudioBackend
        assert 'sounddevice' not in sys.modules
        import sounddevice
        with patch.object(sounddevice, 'RawOutputStream') as factory:
            stream = factory.return_value
            stream.write.return_value = False
            audio = BlockingAudioBackend()
            audio.initialize()
            clip = audio.load_clip(AudioClipDescriptor('tone', 2 / 44100), b'\x01\x00' * 2)
            audio.play(clip)
            audio.pump(2)
            audio.close()
            audio.close()
            assert factory.call_args.kwargs['callback'] is None
            assert factory.call_args.kwargs['finished_callback'] is None
            stream.write.assert_called_once_with(b'\x01\x00' * 2)
            stream.abort.assert_called_once()
            stream.close.assert_called_once()
        assert 'numpy' not in sys.modules
    """)
    with tempfile.TemporaryDirectory(prefix="ludoweave-audio-wheel-") as directory:
        work = Path(directory)
        environment = work / "environment"
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        commands = [
            [uv, "venv", "--python", sys.executable, str(environment)],
            [
                uv,
                "pip",
                "install",
                "--python",
                str(python),
                "--only-binary",
                ":all:",
                f"{wheels[0]}[audio]",
            ],
            [str(python), "-I", "-c", probe],
        ]
        for command in commands:
            subprocess.run(command, cwd=work, check=True)
    print(
        json.dumps(
            {"schema": "ludoweave.audio-wheel-smoke/1", "status": "pass", "physical_output": False},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
