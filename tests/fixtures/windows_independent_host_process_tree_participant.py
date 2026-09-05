"""Fixed process-tree participant for the M211 Windows containment probe."""

from __future__ import annotations

import ctypes
import json
import msvcrt
import os
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from ctypes import wintypes
from pathlib import Path
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-independent-host-process-tree/1"
_CREATE_NO_WINDOW = 0x08000000


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _StartupInfoW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class _ProcessInformation(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


def _load_function(
    library: ctypes.CDLL,
    name: str,
    argument_types: list[object],
    return_type: object,
) -> _NativeFunction:
    function = cast(_NativeFunction, getattr(library, name))
    function.argtypes = argument_types
    function.restype = return_type
    return function


def _emit_to_handle(document: Mapping[str, object], output_handle: int) -> None:
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    descriptor = msvcrt.open_osfhandle(output_handle, os.O_WRONLY)
    try:
        os.write(descriptor, encoded + b"\n")
    finally:
        os.close(descriptor)


def _wait_forever() -> None:
    while True:
        time.sleep(60.0)


def _run_descendant(output_handle: int) -> int:
    _emit_to_handle(
        {
            "event": "descendant_ready",
            "pid": os.getpid(),
            "schema": _SCHEMA,
        },
        output_handle,
    )
    _wait_forever()
    return 0


def _spawn_descendant(output_handle: int) -> tuple[int, int] | None:
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw.is_file():
        return None
    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    kernel32 = win_dll("kernel32", use_last_error=True)
    create_process = _load_function(
        kernel32,
        "CreateProcessW",
        [
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            ctypes.c_void_p,
            ctypes.c_void_p,
            wintypes.BOOL,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.LPCWSTR,
            ctypes.POINTER(_StartupInfoW),
            ctypes.POINTER(_ProcessInformation),
        ],
        wintypes.BOOL,
    )
    close_handle = _load_function(
        kernel32,
        "CloseHandle",
        [wintypes.HANDLE],
        wintypes.BOOL,
    )
    command_line = ctypes.create_unicode_buffer(
        subprocess.list2cmdline(
            (str(pythonw), "-I", "-B", __file__, "descendant", str(output_handle))
        )
    )
    startup = _StartupInfoW()
    startup.cb = ctypes.sizeof(startup)
    process_information = _ProcessInformation()
    os.set_handle_inheritable(output_handle, True)
    try:
        created = cast(
            bool,
            create_process(
                str(pythonw),
                command_line,
                None,
                None,
                True,
                _CREATE_NO_WINDOW,
                None,
                None,
                ctypes.byref(startup),
                ctypes.byref(process_information),
            ),
        )
    finally:
        os.set_handle_inheritable(output_handle, False)
    if not created:
        return None
    if not cast(bool, close_handle(process_information.hThread)):
        return None
    process_handle = process_information.hProcess
    if process_handle is None:
        return None
    return process_information.dwProcessId, process_handle


def _run_participant(output_handle: int) -> int:
    spawned = _spawn_descendant(output_handle)
    if spawned is None:
        return 3
    descendant_pid, descendant_handle = spawned
    _emit_to_handle(
        {
            "descendant_pid": descendant_pid,
            "event": "participant_ready",
            "pid": os.getpid(),
            "schema": _SCHEMA,
        },
        output_handle,
    )
    if descendant_handle <= 0:
        return 3
    _wait_forever()
    return 0


def main() -> int:
    if (
        len(sys.argv) == 3
        and sys.argv[1] in {"participant", "descendant"}
        and sys.argv[2].isdigit()
    ):
        output_handle = int(sys.argv[2])
        if output_handle > 0:
            if sys.argv[1] == "participant":
                return _run_participant(output_handle)
            return _run_descendant(output_handle)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
