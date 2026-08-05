# Third-party notices

The baseline `ludoweave` wheel has no runtime dependencies and redistributes no
third-party Python packages. Contributor, documentation, and optional graphics
environments are resolved separately from `uv.lock` under their own licenses.

The optional `graphics` extra selects these direct packages:

| Package | Locked version | Declared license | Project |
| --- | ---: | --- | --- |
| glfw | 2.10.2 | MIT | <https://github.com/FlorianRhiem/pyGLFW> |
| rendercanvas | 2.7.2 | BSD-2-Clause | <https://github.com/pygfx/rendercanvas> |
| wgpu | 0.32.0 | BSD-2-Clause | <https://github.com/pygfx/wgpu-py> |

Those packages and their transitive/native components are not copied into
LudoWeave release artifacts. Installers obtain their license texts and notices
from the corresponding distributions. This inventory does not replace those
license files or provide legal advice.
