"""Original lightweight line icons, drawn without external icon resources."""

from __future__ import annotations

from typing import Literal

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap, QPolygonF

from python_ui_library.theme.install import _current_theme

IconName = Literal["grid", "folder", "list", "settings", "plus", "search", "info", "check"]


def make_icon(name: IconName, *, color: str | None = None, size: int = 20) -> QIcon:
    """Produce a consistent 1.7px-stroke icon; all paths were drawn for this package."""
    if name not in ("grid", "folder", "list", "settings", "plus", "search", "info", "check"):
        raise ValueError(f"unsupported icon: {name}")
    if size < 12:
        raise ValueError("size must be at least 12 logical pixels")
    if color is None:
        color = _current_theme().colors.text_muted
    if not QColor(color).isValid():
        raise ValueError("color must be a Qt-valid color")
    pix = QPixmap(size * 2, size * 2)
    pix.fill(Qt.GlobalColor.transparent)
    pix.setDevicePixelRatio(2)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(size / 20, size / 20)
    pen = QPen(QColor(color), 1.7)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    if name == "grid":
        for x in (3.5, 11):
            for y in (3.5, 11):
                painter.drawRoundedRect(QRectF(x, y, 5.5, 5.5), 1.2, 1.2)
    elif name == "folder":
        painter.drawPath(_folder_path())
    elif name == "list":
        for y in (5, 10, 15):
            painter.drawLine(QPointF(8, y), QPointF(17, y))
            painter.drawEllipse(QPointF(4.5, y), 0.65, 0.65)
    elif name == "settings":
        painter.drawEllipse(QPointF(10, 10), 6.5, 6.5)
        painter.drawEllipse(QPointF(10, 10), 2.25, 2.25)
        for x1, y1, x2, y2 in (
            (10, 1, 10, 3.5),
            (10, 16.5, 10, 19),
            (1, 10, 3.5, 10),
            (16.5, 10, 19, 10),
        ):
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    elif name == "plus":
        painter.drawLine(QPointF(10, 4), QPointF(10, 16))
        painter.drawLine(QPointF(4, 10), QPointF(16, 10))
    elif name == "search":
        painter.drawEllipse(QPointF(8.4, 8.4), 5.2, 5.2)
        painter.drawLine(QPointF(12.3, 12.3), QPointF(17, 17))
    elif name == "info":
        painter.drawEllipse(QPointF(10, 10), 8, 8)
        painter.drawLine(QPointF(10, 9), QPointF(10, 14))
        painter.drawPoint(QPointF(10, 6))
    elif name == "check":
        painter.drawPolyline(QPolygonF([QPointF(3, 10), QPointF(8, 15), QPointF(17, 5)]))
    painter.end()
    return QIcon(pix)


def _folder_path():
    from PySide6.QtGui import QPainterPath

    path = QPainterPath()
    path.moveTo(2.5, 6)
    path.lineTo(2.5, 15)
    path.quadTo(2.5, 17, 4.5, 17)
    path.lineTo(16, 17)
    path.quadTo(18, 17, 18, 15)
    path.lineTo(18, 7.5)
    path.quadTo(18, 6, 16.5, 6)
    path.lineTo(10, 6)
    path.lineTo(8, 3.5)
    path.lineTo(4.5, 3.5)
    path.quadTo(2.5, 3.5, 2.5, 6)
    return path
