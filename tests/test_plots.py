from __future__ import annotations

from dataclasses import replace

import pytest
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QWidget

from alp_ui.components import Plot
from alp_ui.theme import ALPACA_LIGHT, install_theme


@pytest.fixture(autouse=True)
def _install_default_theme(qapp: QApplication) -> None:
    install_theme(qapp)


def _foreground_pixels(plot: Plot) -> int:
    image = plot.grab().toImage()
    surface = image.pixelColor(0, 0).rgb()
    return sum(
        image.pixelColor(x, y).rgb() != surface
        for y in range(image.height())
        for x in range(image.width())
    )


def test_line_plot_validates_updates_accessibility_and_draws(qtbot) -> None:
    plot = Plot(kind="line", x_label="Time", y_label="Value")
    qtbot.addWidget(plot)
    plot.resize(480, 280)
    empty_pixels = _foreground_pixels(plot)

    plot.setAccessibleName("Observed measurements")
    plot.setLines(
        {
            "Observed": [(0.0, -0.2), (1.0, 0.4), (2.0, 0.4)],
            "Reference": [(0.0, 0.1), (1.0, 0.2)],
        }
    )

    assert plot.accessibleName() == "Observed measurements"
    assert plot.accessibleDescription() == "Line plot with 2 series and 5 points."
    assert plot.sizeHint().width() > plot.minimumSizeHint().width()
    assert not plot.findChildren(QWidget)
    assert not plot.findChildren(QTimer)
    assert _foreground_pixels(plot) > empty_pixels + 100


def test_empty_bar_and_hundreds_of_ordered_line_points_render_without_children(qtbot) -> None:
    bar = Plot(kind="bar")
    qtbot.addWidget(bar)
    bar.resize(300, 200)
    bar.setBars([])
    assert bar.accessibleDescription() == "Bar plot with no data."
    assert _foreground_pixels(bar) > 0

    line = Plot(kind="line")
    qtbot.addWidget(line)
    line.resize(480, 280)
    line.setLines(
        {
            "Observed": [(float(index), float(index % 11)) for index in range(400)],
            "Reference": [(float(index), float((index * 3) % 13)) for index in range(400)],
        }
    )
    assert line.accessibleDescription() == "Line plot with 2 series and 800 points."
    assert not line.findChildren(QWidget)
    assert not line.grab().isNull()


@pytest.mark.parametrize(
    ("kind", "method", "data", "error"),
    [
        ("bar", "setBars", [("A", float("nan"))], ValueError),
        ("bar", "setBars", [("A", float("inf"))], ValueError),
        ("bar", "setBars", [("A", "1")], TypeError),
        ("bar", "setBars", [("", 1)], ValueError),
        ("line", "setLines", {"A": [(0, 1, 2)]}, TypeError),
        ("line", "setLines", {"A": [(0, None)]}, TypeError),
    ],
)
def test_plot_rejects_invalid_data_before_replacing_state(
    kind: str, method: str, data: object, error: type[Exception]
) -> None:
    plot = Plot(kind=kind)  # type: ignore[arg-type]
    if kind == "bar":
        plot.setBars([("First", 1.0)])
    else:
        plot.setLines({"First": [(0.0, 1.0)]})
    previous_description = plot.accessibleDescription()

    with pytest.raises(error):
        getattr(plot, method)(data)

    assert plot.accessibleDescription() == previous_description


def test_plot_rejects_wrong_kind_and_invalid_kind() -> None:
    with pytest.raises(ValueError, match="kind must be one of"):
        Plot(kind="scatter")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="only available"):
        Plot(kind="line").setBars([])
    with pytest.raises(ValueError, match="only available"):
        Plot(kind="bar").setLines({})


def test_bar_plot_preserves_category_order_in_tooltip_and_handles_ranges(qtbot) -> None:
    plot = Plot(kind="bar", x_label="Category", y_label="Value")
    qtbot.addWidget(plot)
    plot.resize(300, 200)
    categories = [
        (f"Long category {index:02d}", value) for index, value in enumerate(range(-10, 11))
    ]
    plot.setBars(categories)

    assert plot.accessibleDescription() == "Bar plot with 21 categories."
    assert plot.toolTip() == "Categories: " + ", ".join(category for category, _ in categories)
    assert _foreground_pixels(plot) > 100


def test_plot_uses_custom_theme_tokens(qapp: QApplication, qtbot) -> None:
    custom = replace(ALPACA_LIGHT, colors=replace(ALPACA_LIGHT.colors, primary="#7C3AED"))
    install_theme(qapp, custom)
    plot = Plot(kind="line")
    qtbot.addWidget(plot)
    plot.resize(480, 280)
    plot.setLines({"Series": [(0.0, 0.0), (1.0, 1.0)]})

    image = plot.grab().toImage()

    assert any(
        image.pixelColor(x, y).name().upper() == custom.colors.primary
        for y in range(image.height())
        for x in range(image.width())
    )


def test_plot_handles_compact_theme_and_narrow_layout(qapp: QApplication, qtbot) -> None:
    install_theme(qapp, replace(ALPACA_LIGHT, density="compact"))
    plot = Plot(kind="bar", x_label="Category", y_label="Value")
    qtbot.addWidget(plot)
    plot.resize(220, 160)
    plot.setBars([(f"A long category {index}", float(index - 10)) for index in range(20)])

    assert not plot.grab().isNull()
