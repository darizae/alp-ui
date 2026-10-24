"""Small, read-only native Qt plots for consumer-supplied data."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Literal

from PySide6.QtCore import QPointF, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QSizePolicy, QWidget

from alp_ui.theme.install import _current_theme

PlotKind = Literal["line", "bar"]
_KINDS = ("line", "bar")
_LINE_STYLES = (
    Qt.PenStyle.SolidLine,
    Qt.PenStyle.DashLine,
    Qt.PenStyle.DotLine,
    Qt.PenStyle.DashDotLine,
)


def _finite_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{label} must be a finite numeric value")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _pair(value: object, label: str) -> tuple[object, object]:
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{label} must be a pair")
    try:
        first, second = value  # type: ignore[misc]
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{label} must be a pair") from exc
    return first, second


def _expanded_range(low: float, high: float) -> tuple[float, float]:
    if low != high:
        return low, high
    padding = max(abs(low) * 0.05, 1.0)
    return low - padding, high + padding


def _tick_label(value: float, step: float) -> str:
    """Keep small values legible without inventing decimal places."""
    magnitude = max(abs(value), abs(step))
    if magnitude and (magnitude >= 10_000 or magnitude < 0.001):
        return f"{value:.3g}"
    decimals = max(0, min(4, int(math.ceil(-math.log10(abs(step)))) if step else 0))
    return f"{value:.{decimals}f}"


class Plot(QWidget):
    """Theme-aware numeric line or categorical bar presentation.

    ``setLines`` renders supplied points in their input order; x values are not sorted.
    ``setBars`` renders supplied category/value pairs in their input order.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        kind: PlotKind = "line",
        x_label: str = "",
        y_label: str = "",
    ) -> None:
        if kind not in _KINDS:
            raise ValueError("kind must be one of: line, bar")
        if not isinstance(x_label, str) or not isinstance(y_label, str):
            raise TypeError("x_label and y_label must be strings")
        super().__init__(parent)
        self.kind: PlotKind = kind
        self.x_label = x_label
        self.y_label = y_label
        self._line_series: tuple[tuple[str, tuple[tuple[float, float], ...]], ...] = ()
        self._bars: tuple[tuple[str, float], ...] = ()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleName(f"{kind.capitalize()} plot")
        self._update_accessibility()

    def setLines(self, lines: Mapping[str, Sequence[object]]) -> None:  # noqa: N802
        """Replace line series after validating every caller-supplied point."""
        if self.kind != "line":
            raise ValueError("setLines is only available when kind is line")
        if not isinstance(lines, Mapping):
            raise TypeError("lines must be an ordered mapping of labels to point sequences")

        prepared: list[tuple[str, tuple[tuple[float, float], ...]]] = []
        for series_label, points in lines.items():
            if not isinstance(series_label, str) or not series_label:
                raise ValueError("line series labels must be nonempty strings")
            if isinstance(points, (str, bytes)) or not isinstance(points, Sequence):
                raise TypeError(f"points for {series_label!r} must be a sequence of pairs")
            series: list[tuple[float, float]] = []
            for point_index, point in enumerate(points):
                x_value, y_value = _pair(point, f"point {point_index} in {series_label!r}")
                series.append(
                    (
                        _finite_number(x_value, f"x at point {point_index} in {series_label!r}"),
                        _finite_number(y_value, f"y at point {point_index} in {series_label!r}"),
                    )
                )
            prepared.append((series_label, tuple(series)))

        self._line_series = tuple(prepared)
        self._update_accessibility()
        self.update()

    def setBars(self, bars: Sequence[object]) -> None:  # noqa: N802
        """Replace categorical bars after validating every caller-supplied value."""
        if self.kind != "bar":
            raise ValueError("setBars is only available when kind is bar")
        if isinstance(bars, (str, bytes)) or not isinstance(bars, Sequence):
            raise TypeError("bars must be a sequence of category/value pairs")

        prepared: list[tuple[str, float]] = []
        for index, bar in enumerate(bars):
            category, value = _pair(bar, f"bar {index}")
            if not isinstance(category, str) or not category:
                raise ValueError("bar categories must be nonempty strings")
            prepared.append((category, _finite_number(value, f"value for bar {category!r}")))

        self._bars = tuple(prepared)
        self.setToolTip("Categories: " + ", ".join(category for category, _ in prepared))
        self._update_accessibility()
        self.update()

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(480, 280)

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        return QSize(220, 160)

    def _update_accessibility(self) -> None:
        if self.kind == "line":
            series_count = len(self._line_series)
            point_count = sum(len(points) for _, points in self._line_series)
            if not series_count:
                description = "Line plot with no data."
            else:
                description = f"Line plot with {series_count} series and {point_count} points."
        else:
            count = len(self._bars)
            description = (
                "Bar plot with no data." if not count else f"Bar plot with {count} categories."
            )
        self.setAccessibleDescription(description)

    def _has_data(self) -> bool:
        return (
            bool(self._bars)
            if self.kind == "bar"
            else any(points for _, points in self._line_series)
        )

    def _line_bounds(self) -> tuple[float, float, float, float]:
        points = [point for _, series in self._line_series for point in series]
        x_values, y_values = zip(*points, strict=True)
        low_x, high_x = _expanded_range(min(x_values), max(x_values))
        low_y, high_y = _expanded_range(min(y_values), max(y_values))
        return low_x, high_x, low_y, high_y

    def _bar_bounds(self) -> tuple[float, float]:
        values = [value for _, value in self._bars]
        return _expanded_range(min(0.0, min(values)), max(0.0, max(values)))

    def _legend_height(self, metrics: QFontMetrics) -> int:
        if self.kind != "line" or not self._line_series:
            return 0
        small, _ = self._plot_spacing()
        return metrics.height() + small

    def _plot_spacing(self) -> tuple[int, int]:
        theme = _current_theme()
        if theme.density == "compact":
            return max(2, theme.spacing.xsmall), max(4, theme.spacing.small)
        return theme.spacing.small, theme.spacing.medium

    def _draw_empty(self, painter: QPainter) -> None:
        theme = _current_theme()
        painter.setPen(QColor(theme.colors.text_muted))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No data to display")

    def _draw_axes(
        self,
        painter: QPainter,
        plot: QRectF,
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        *,
        draw_x_ticks: bool = True,
    ) -> None:
        theme = _current_theme()
        metrics = QFontMetrics(self.font())
        text_color = QColor(theme.colors.text_muted)
        grid_pen = QPen(QColor(theme.colors.border), 1)
        axis_pen = QPen(text_color, 1)
        x_low, x_high = x_range
        y_low, y_high = y_range
        x_step = (x_high - x_low) / 4
        y_step = (y_high - y_low) / 4

        painter.setPen(grid_pen)
        for index in range(5):
            fraction = index / 4
            x = plot.left() + fraction * plot.width()
            y = plot.bottom() - fraction * plot.height()
            painter.drawLine(QPointF(x, plot.top()), QPointF(x, plot.bottom()))
            painter.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))

        painter.setPen(axis_pen)
        painter.drawLine(QPointF(plot.left(), plot.bottom()), QPointF(plot.right(), plot.bottom()))
        painter.drawLine(QPointF(plot.left(), plot.top()), QPointF(plot.left(), plot.bottom()))
        for index in range(5):
            fraction = index / 4
            x = plot.left() + fraction * plot.width()
            y = plot.bottom() - fraction * plot.height()
            y_text = _tick_label(y_low + fraction * (y_high - y_low), y_step)
            if draw_x_ticks:
                x_text = _tick_label(x_low + fraction * (x_high - x_low), x_step)
                painter.drawText(
                    QRectF(x - 35, plot.bottom() + 2, 70, metrics.height()),
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                    x_text,
                )
            painter.drawText(
                QRectF(0, y - metrics.height() / 2, plot.left() - 6, metrics.height()),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                y_text,
            )

        if self.x_label:
            painter.drawText(
                QRectF(
                    plot.left(),
                    plot.bottom() + (metrics.height() if draw_x_ticks else 0) + 2,
                    plot.width(),
                    metrics.height(),
                ),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                self.x_label,
            )
        if self.y_label:
            painter.save()
            painter.translate(metrics.height(), plot.center().y())
            painter.rotate(-90)
            painter.drawText(
                QRectF(-plot.height() / 2, -metrics.height() / 2, plot.height(), metrics.height()),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                self.y_label,
            )
            painter.restore()

    def _draw_legend(self, painter: QPainter, top: int) -> None:
        if self.kind != "line" or not self._line_series:
            return
        theme = _current_theme()
        metrics = QFontMetrics(self.font())
        available = max(40, self.width() // max(1, len(self._line_series)) - 28)
        _, medium = self._plot_spacing()
        x = medium
        colors = (
            theme.colors.primary,
            theme.colors.info,
            theme.colors.text_muted,
            theme.colors.danger,
        )
        for index, (label, _) in enumerate(self._line_series):
            painter.setPen(
                QPen(
                    QColor(colors[index % len(colors)]), 2, _LINE_STYLES[index % len(_LINE_STYLES)]
                )
            )
            painter.drawLine(
                QPointF(x, top + metrics.height() / 2), QPointF(x + 16, top + metrics.height() / 2)
            )
            painter.setPen(QColor(theme.colors.text_muted))
            painter.drawText(
                QRectF(x + 20, top, available, metrics.height()),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                metrics.elidedText(label, Qt.TextElideMode.ElideRight, available),
            )
            x += available + 28

    def _draw_lines(
        self, painter: QPainter, plot: QRectF, bounds: tuple[float, float, float, float]
    ) -> None:
        theme = _current_theme()
        low_x, high_x, low_y, high_y = bounds
        colors = (
            theme.colors.primary,
            theme.colors.info,
            theme.colors.text_muted,
            theme.colors.danger,
        )

        def mapped(point: tuple[float, float]) -> QPointF:
            x_value, y_value = point
            return QPointF(
                plot.left() + (x_value - low_x) / (high_x - low_x) * plot.width(),
                plot.bottom() - (y_value - low_y) / (high_y - low_y) * plot.height(),
            )

        painter.save()
        painter.setClipRect(plot)
        for index, (_, points) in enumerate(self._line_series):
            if not points:
                continue
            color = QColor(colors[index % len(colors)])
            painter.setPen(QPen(color, 2, _LINE_STYLES[index % len(_LINE_STYLES)]))
            mapped_points = [mapped(point) for point in points]
            if len(mapped_points) > 1:
                painter.drawPolyline(QPolygonF(mapped_points))
            painter.setBrush(color)
            for point in mapped_points:
                painter.drawEllipse(point, 2.5, 2.5)
        painter.restore()

    def _draw_bars(self, painter: QPainter, plot: QRectF, low: float, high: float) -> None:
        theme = _current_theme()
        metrics = QFontMetrics(self.font())
        baseline = plot.bottom() - (0.0 - low) / (high - low) * plot.height()
        slot = plot.width() / len(self._bars)
        bar_width = max(1.0, slot * 0.7)
        color = QColor(theme.colors.text_muted)
        painter.save()
        painter.setClipRect(plot)
        painter.setPen(QPen(color, 1))
        painter.setBrush(color)
        for index, (_, value) in enumerate(self._bars):
            x = plot.left() + index * slot + (slot - bar_width) / 2
            value_y = plot.bottom() - (value - low) / (high - low) * plot.height()
            height = abs(value_y - baseline)
            if height:
                painter.drawRect(QRectF(x, min(value_y, baseline), bar_width, height))
        painter.restore()
        painter.setPen(QColor(theme.colors.text_muted))
        for index, (category, _) in enumerate(self._bars):
            x = plot.left() + index * slot
            text = metrics.elidedText(category, Qt.TextElideMode.ElideRight, max(1, int(slot)))
            painter.drawText(
                QRectF(x, plot.bottom() + 2, slot, metrics.height()),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                text,
            )

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        theme = _current_theme()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(theme.colors.surface))
        if not self._has_data():
            self._draw_empty(painter)
            return

        metrics = QFontMetrics(self.font())
        legend_height = self._legend_height(metrics)
        small, medium = self._plot_spacing()
        left = max(48, metrics.horizontalAdvance("-0000") + metrics.height() + small * 2)
        plot = QRectF(
            left,
            legend_height + small,
            self.width() - left - medium,
            self.height() - legend_height - metrics.height() * 3 - medium,
        )
        if plot.width() < 24 or plot.height() < 24:
            self._draw_empty(painter)
            return

        painter.setPen(QColor(theme.colors.text_muted))
        self._draw_legend(painter, 0)
        if self.kind == "line":
            low_x, high_x, low_y, high_y = self._line_bounds()
            self._draw_axes(painter, plot, (low_x, high_x), (low_y, high_y))
            self._draw_lines(painter, plot, (low_x, high_x, low_y, high_y))
        else:
            low, high = self._bar_bounds()
            self._draw_axes(
                painter,
                plot,
                (0.0, float(len(self._bars))),
                (low, high),
                draw_x_ticks=False,
            )
            self._draw_bars(painter, plot, low, high)
