from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

FONT: Font = Font(
    name="Calibri",
    bold=True,
    italic=False,
    vertAlign=None,
    underline="none",
    strike=False,
)

BORDER_LINE: Side = Side(border_style="thin", color="000000")

TITLE_HEIGHT: int = 25
TITLE_FONT: Font = FONT
TITLE_FONT.size = 13
TITLE_FILL: PatternFill = PatternFill(patternType="solid", fgColor="b4c7dc")

HEADERS_HEIGHT: int = 20
HEADERS_FONT: Font = FONT
HEADERS_FONT.size = 12
HEADERS_FILL: PatternFill = PatternFill(patternType="solid", fgColor="2a6099")
HEADERS_BORDER: Border = Border(
    top=BORDER_LINE,
    bottom=BORDER_LINE,
    left=BORDER_LINE,
    right=BORDER_LINE,
)

ALIGNMENT_CENTER: Alignment = Alignment(
    horizontal="general",
    vertical="center",
    text_rotation=0,
    wrap_text=False,
    shrink_to_fit=False,
    indent=0,
)

ROWS_FILL: PatternFill = PatternFill(patternType="solid", fgColor="dee6ef")
