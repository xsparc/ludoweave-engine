"""Deterministic bitmap-font layout and sprite extraction."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ludoweave.presentation._validation import (
    bounded_int,
    finite_float,
    freeze_bounded_exact,
    normalized_uv,
    stable_name,
)
from ludoweave.presentation.errors import presentation_error
from ludoweave.render.contracts import Color
from ludoweave.render.extraction import SpriteExtractionSource
from ludoweave.render.handles import TextureHandle

_MAX_TEXT_CODEPOINTS = 4096
_MAX_LAYOUT_GLYPHS = _MAX_TEXT_CODEPOINTS * 4
_MAX_GLYPHS = 4096
_MAX_LINES = 256
_WHITE = Color(1.0, 1.0, 1.0, 1.0)


class TextAlign(StrEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


@dataclass(frozen=True, slots=True)
class BitmapGlyph:
    """Integer layout metrics plus one normalized atlas rectangle."""

    character: str
    advance: int
    width: int
    height: int
    offset_x: int
    offset_y: int
    uv_left: float
    uv_top: float
    uv_right: float
    uv_bottom: float

    def __post_init__(self) -> None:
        if (
            type(self.character) is not str
            or len(self.character) != 1
            or self.character in "\r\n\t"
            or not self.character.isprintable()
        ):
            raise presentation_error(
                "bitmap glyph keys must be one printable code point",
                phase="text_glyph",
                details={"field": "character"},
            )
        bounded_int(self.advance, phase="text_glyph", field="advance", maximum=2**16 - 1)
        bounded_int(self.width, phase="text_glyph", field="width", maximum=2**16 - 1)
        bounded_int(self.height, phase="text_glyph", field="height", maximum=2**16 - 1)
        if (self.width == 0) != (self.height == 0):
            raise presentation_error(
                "bitmap glyph dimensions must both be zero or both be positive",
                phase="text_glyph",
                details={"field": "size"},
            )
        bounded_int(
            self.offset_x,
            phase="text_glyph",
            field="offset_x",
            minimum=-(2**15),
            maximum=2**15 - 1,
        )
        bounded_int(
            self.offset_y,
            phase="text_glyph",
            field="offset_y",
            minimum=-(2**15),
            maximum=2**15 - 1,
        )
        normalized_uv(
            self.uv_left,
            self.uv_top,
            self.uv_right,
            self.uv_bottom,
            phase="text_glyph",
        )

    @property
    def visible(self) -> bool:
        return self.width > 0


@dataclass(frozen=True, slots=True)
class BitmapFont:
    """A bounded caller-loaded atlas description; no font parser is implied."""

    name: str
    line_height: int
    glyphs: tuple[BitmapGlyph, ...]
    fallback_character: str

    def __post_init__(self) -> None:
        stable_name(self.name, phase="text_font")
        bounded_int(
            self.line_height,
            phase="text_font",
            field="line_height",
            minimum=1,
            maximum=2**16 - 1,
        )
        glyphs = freeze_bounded_exact(
            self.glyphs,
            BitmapGlyph,
            maximum=_MAX_GLYPHS,
            phase="text_font",
            field="glyphs",
        )
        characters = tuple(glyph.character for glyph in glyphs)
        if len(set(characters)) != len(characters):
            raise presentation_error(
                "bitmap font glyph keys must be unique",
                phase="text_font",
                details={"field": "glyphs"},
            )
        if type(self.fallback_character) is not str or self.fallback_character not in characters:
            raise presentation_error(
                "bitmap font fallback must identify one declared glyph",
                phase="text_font",
                details={"field": "fallback_character"},
            )
        object.__setattr__(self, "glyphs", glyphs)


@dataclass(frozen=True, slots=True)
class GlyphPlacement:
    character: str
    glyph: BitmapGlyph
    x: int
    y: int
    line: int

    def __post_init__(self) -> None:
        if type(self.character) is not str or len(self.character) != 1:
            raise presentation_error(
                "glyph placement requires one source character",
                phase="text_layout",
                details={"field": "character"},
            )
        if type(self.glyph) is not BitmapGlyph:
            raise presentation_error(
                "glyph placement requires an exact bitmap glyph",
                phase="text_layout",
                details={"field": "glyph"},
            )
        bounded_int(
            self.x,
            phase="text_layout",
            field="x",
            minimum=-(2**31),
            maximum=2**31 - 1,
        )
        bounded_int(
            self.y,
            phase="text_layout",
            field="y",
            minimum=-(2**31),
            maximum=2**31 - 1,
        )
        bounded_int(self.line, phase="text_layout", field="line", maximum=_MAX_LINES - 1)


@dataclass(frozen=True, slots=True)
class TextLayout:
    """Detached layout result using integer authoring units."""

    placements: tuple[GlyphPlacement, ...]
    line_widths: tuple[int, ...]
    width: int
    height: int

    def __post_init__(self) -> None:
        placements = freeze_bounded_exact(
            self.placements,
            GlyphPlacement,
            maximum=_MAX_LAYOUT_GLYPHS,
            phase="text_layout",
            field="placements",
            allow_empty=True,
        )
        widths = freeze_bounded_exact(
            self.line_widths,
            int,
            maximum=_MAX_LINES,
            phase="text_layout",
            field="line_widths",
        )
        if any(width < 0 for width in widths):
            raise presentation_error(
                "text layout requires bounded non-negative line widths",
                phase="text_layout",
                details={"field": "line_widths"},
            )
        if any(item.line >= len(widths) for item in placements) or tuple(
            item.line for item in placements
        ) != tuple(sorted(item.line for item in placements)):
            raise presentation_error(
                "text placements must use declared lines in canonical order",
                phase="text_layout",
                details={"field": "placements"},
            )
        bounded_int(self.width, phase="text_layout", field="width", maximum=2**31 - 1)
        if self.width < max(widths):
            raise presentation_error(
                "text layout width cannot be smaller than its content",
                phase="text_layout",
                details={"field": "width"},
            )
        bounded_int(
            self.height,
            phase="text_layout",
            field="height",
            minimum=1,
            maximum=2**31 - 1,
        )
        object.__setattr__(self, "placements", placements)
        object.__setattr__(self, "line_widths", widths)


def layout_text(
    font: BitmapFont,
    text: str,
    *,
    max_width: int | None = None,
    max_lines: int = _MAX_LINES,
    align: TextAlign = TextAlign.LEFT,
) -> TextLayout:
    """Lay out code points with explicit newlines and deterministic glyph wrapping."""

    if type(font) is not BitmapFont:
        raise presentation_error(
            "text layout requires an exact bitmap font",
            phase="text_layout",
            details={"field": "font", "actual_type": type(font).__name__},
        )
    if type(text) is not str or not text or len(text) > _MAX_TEXT_CODEPOINTS:
        raise presentation_error(
            "text input must be bounded non-empty Unicode text",
            phase="text_layout",
            details={"field": "text", "maximum": _MAX_TEXT_CODEPOINTS},
        )
    if any(not character.isprintable() and character not in "\n\t" for character in text):
        raise presentation_error(
            "text input contains an unsupported control code point",
            phase="text_layout",
            details={"field": "text"},
        )
    checked_width = (
        None
        if max_width is None
        else bounded_int(
            max_width,
            phase="text_layout",
            field="max_width",
            minimum=1,
            maximum=2**31 - 1,
        )
    )
    checked_lines = bounded_int(
        max_lines,
        phase="text_layout",
        field="max_lines",
        minimum=1,
        maximum=_MAX_LINES,
    )
    if type(align) is not TextAlign:
        raise presentation_error(
            "text alignment must be an exact TextAlign",
            phase="text_layout",
            details={"field": "align", "actual_type": type(align).__name__},
        )

    glyph_by_character = {glyph.character: glyph for glyph in font.glyphs}
    fallback = glyph_by_character[font.fallback_character]
    expanded = text.replace("\t", "    ")
    raw: list[GlyphPlacement] = []
    widths = [0]
    line = 0
    for character in expanded:
        if character == "\n":
            line += 1
            _require_line(line, checked_lines)
            widths.append(0)
            continue
        glyph = glyph_by_character.get(character, fallback)
        if checked_width is not None and glyph.advance > checked_width:
            raise presentation_error(
                "one glyph advance exceeds the configured layout width",
                phase="text_layout",
                details={"field": "max_width", "character": character},
            )
        if (
            checked_width is not None
            and widths[line] > 0
            and widths[line] + glyph.advance > checked_width
        ):
            line += 1
            _require_line(line, checked_lines)
            widths.append(0)
        raw.append(
            GlyphPlacement(
                character,
                glyph,
                widths[line] + glyph.offset_x,
                line * font.line_height + glyph.offset_y,
                line,
            )
        )
        widths[line] += glyph.advance

    container_width = checked_width if checked_width is not None else max(widths)
    aligned = tuple(
        GlyphPlacement(
            placement.character,
            placement.glyph,
            placement.x + _alignment_offset(container_width, widths[placement.line], align),
            placement.y,
            placement.line,
        )
        for placement in raw
    )
    return TextLayout(
        aligned,
        tuple(widths),
        container_width,
        len(widths) * font.line_height,
    )


def glyph_sprites(
    texture: TextureHandle,
    layout: TextLayout,
    *,
    base_entity_index: int,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    tint: Color = _WHITE,
    layer: int = 0,
    z: float = 0.0,
) -> tuple[SpriteExtractionSource, ...]:
    """Convert visible bitmap glyphs to existing renderer-neutral sprites."""

    if type(layout) is not TextLayout:
        raise presentation_error(
            "glyph extraction requires an exact TextLayout",
            phase="text_extract",
            details={"field": "layout", "actual_type": type(layout).__name__},
        )
    if type(texture) is not TextureHandle:
        raise presentation_error(
            "glyph extraction requires an exact texture handle",
            phase="text_extract",
            details={"field": "texture", "actual_type": type(texture).__name__},
        )
    for field, value in (("origin_x", origin_x), ("origin_y", origin_y), ("z", z)):
        finite_float(value, phase="text_extract", field=field)
    bounded_int(layer, phase="text_extract", field="layer")
    if type(tint) is not Color:
        raise presentation_error(
            "glyph extraction tint must be an exact Color",
            phase="text_extract",
            details={"field": "tint"},
        )
    bounded_int(
        base_entity_index,
        phase="text_extract",
        field="base_entity_index",
        maximum=2**63 - 1,
    )
    visible = tuple(item for item in layout.placements if item.glyph.visible)
    if visible and base_entity_index + len(visible) - 1 > 2**63 - 1:
        raise presentation_error(
            "glyph entity identity range exceeds signed 64-bit bounds",
            phase="text_extract",
            details={"field": "base_entity_index"},
        )
    sources: list[SpriteExtractionSource] = []
    for ordinal, placement in enumerate(visible):
        glyph = placement.glyph
        x = origin_x + float(placement.x) + float(glyph.width) / 2.0
        y = origin_y + float(placement.y) + float(glyph.height) / 2.0
        sources.append(
            SpriteExtractionSource(
                texture,
                base_entity_index + ordinal,
                0,
                x,
                y,
                x,
                y,
                0.0,
                0.0,
                float(glyph.width),
                float(glyph.height),
                glyph.uv_left,
                glyph.uv_top,
                glyph.uv_right,
                glyph.uv_bottom,
                tint,
                layer,
                z,
            )
        )
    return tuple(sources)


def _require_line(line: int, maximum: int) -> None:
    if line >= maximum:
        raise presentation_error(
            "text layout exceeds the configured line bound",
            phase="text_layout",
            details={"field": "max_lines", "maximum": maximum},
        )


def _alignment_offset(container: int, content: int, align: TextAlign) -> int:
    remaining = container - content
    if align is TextAlign.CENTER:
        return remaining // 2
    if align is TextAlign.RIGHT:
        return remaining
    return 0
