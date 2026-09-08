# RFC-0220: bounded optional blocking audio

Status: accepted for M238 implementation by the maintainer on 2026-09-09.

## Motivation

M4-04 requires a sample that plays sound without Python callback work in the
real-time path. Null validation alone did not satisfy audible playback. Admit
one optional provider, not a platform replacement or canonical-state change.

## DirectionBriefV1

- schema_version: 1
- baseline_commit: `960158196a3d69a14dc351c837cdb908f1eac9d4`
- scanned_at: 2026-09-09
- coverage: wheels, native callback source, ownership, PCM delivery and licensing.
- Finding (reject): pygame-ce 2.5.8 has broad wheel coverage, but its completion
  callback acquires the GIL and clears Python references, conflicting with the
  callback boundary. Source event date: 2026-08-09 (2.5.8). High confidence from its
  [mixer source](https://github.com/pygame-community/pygame-ce/blob/2.5.8/src_c/mixer.c).
  Avoiding this would require provider surgery; no roadmap admission.
- Finding (adopt): sounddevice 0.5.6 supports raw bytes and blocking writes
  without NumPy. `callback=None` supplies a null native callback;
  `finished_callback=None` installs no completion callback. Source event:
  2026-08-17 (0.5.6). High confidence from
  [source](https://github.com/spatialaudio/python-sounddevice/blob/0.5.6/sounddevice.py)
  and [raw-stream docs](https://python-sounddevice.readthedocs.io/en/0.5.6/api/raw-streams.html).
  Alignment: optional real sound with explicit ownership. Cost: bounded mixing
  and an explicit pump. Risk: driver latency/underruns. Roadmap delta: M238 only;
  verification requires lifecycle, installed artifact and device execution.
- Finding (adopt): the MIT-licensed provider publishes universal Python wheels
  with PortAudio bundled on Windows/macOS; Linux needs system PortAudio. See
  [release files](https://pypi.org/project/sounddevice/0.5.6/#files) and
  [installation](https://python-sounddevice.readthedocs.io/en/0.5.6/installation.html).
  Source event date: 2026-08-17 (0.5.6). High confidence for packaging, pending hosted
  execution. Supported wheel installs need no compiler; CFFI is optional and
  transitive. Cost: one extra and steps in existing jobs, no added allocation.
- overall_recommendation: adopt pumped raw output, retain Null.
- evidence_gaps: hosted execution remains distinct from local device writes and
  listening confirmation. Package metadata does not prove audible output.

## Contract

Input is immutable raw mono PCM16, signed little-endian at 44,100 Hz. Duration
must agree with sample count within half a sample. Limits: 64 clips, ten seconds
per clip, 16 MiB total PCM and 16 voices. Exhaustion refuses with
`audio.capacity_exceeded`; voices are not stolen. No file parser or resampler.

The constructing thread owns all operations. Pump mixes 1..4096 frames with
gain multiplication and signed-16 saturation, then writes native-endian PCM.
Completed one-shot handles expire after pump; loops remain until stopped.
Buffering can delay already-written sound after controls change. Close aborts
buffered output and closes once. Initialization/write failures close resources
and chain the cause into `audio.provider_failure`; cleanup failure does not
mask the original cause. Only the owned stream is affected, not other streams.
There is no worker and no portable hard timeout for blocking driver calls.

## Qualification

Fake-output tests cover samples, gains, saturation, looping, completion, limits,
handles, failures and thread ownership. Provider wiring asserts callbacks absent.
Device runs and human listening are separate observations. Compare canonical
sample summaries across modes and validate the installed wheel. Existing
Linux/macOS/Windows jobs exercise provider wiring without presuming hardware;
no new hosted job is introduced.
