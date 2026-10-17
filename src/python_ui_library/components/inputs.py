"""Generic form components composed from native Qt controls."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from PySide6.QtCore import QAbstractItemModel, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPalette, QPen, QValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QCompleter,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from python_ui_library.theme.install import _current_theme

NumberKind = Literal["integer", "decimal"]
_NUMBER_KINDS = ("integer", "decimal")


def _plain_label_text(text: str) -> str:
    return text.replace("&&", "\0").replace("&", "").replace("\0", "&")


def _style_control(control: QWidget, selector: str) -> None:
    theme = _current_theme()
    colors = theme.colors
    font = QFont(control.font())
    font.setPointSizeF(theme.typography.body_size)
    font.setWeight(QFont.Weight(theme.typography.body_weight))
    control.setFont(font)

    palette = control.palette()
    palette.setColor(QPalette.ColorRole.Base, QColor(colors.surface))
    palette.setColor(QPalette.ColorRole.Text, QColor(colors.text))
    palette.setColor(QPalette.ColorRole.Button, QColor(colors.surface))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors.text))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors.text_muted))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(colors.primary))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors.on_primary))
    control.setPalette(palette)

    # Local QSS supplies the compact outline and a focus/error border across native styles.
    control.setStyleSheet(
        f"""
        {selector} {{
            background-color: {colors.surface};
            color: {colors.text};
            border: 1px solid {colors.border};
            border-radius: {theme.radii.button}px;
            padding: {theme.spacing.xsmall}px {theme.spacing.small}px;
        }}
        {selector}:focus {{
            border: 2px solid {colors.info};
        }}
        {selector}[invalid="true"] {{
            border-color: {colors.danger};
        }}
        {selector}:disabled {{
            background-color: {colors.background};
            color: {colors.text_muted};
            border-color: {colors.border};
        }}
        """
    )


class _Field(QWidget):
    """Small shared label/description/error composition for native controls."""

    def __init__(
        self,
        control: QWidget,
        *,
        label: str,
        description: str,
        error: str,
        parent: QWidget | None,
    ) -> None:
        super().__init__(parent)
        self.control = control
        self.label_widget = QLabel(self)
        self.description_widget = QLabel(self)
        self.error_widget = QLabel(self)

        theme = _current_theme()
        label_font = QFont(self.label_widget.font())
        label_font.setPointSizeF(theme.typography.body_size)
        label_font.setWeight(QFont.Weight(theme.typography.button_weight))
        self.label_widget.setFont(label_font)
        self.label_widget.setWordWrap(True)

        message_font = QFont(self.description_widget.font())
        message_font.setPointSizeF(theme.typography.overline_size)
        self.description_widget.setFont(message_font)
        self.error_widget.setFont(message_font)
        for widget, color in (
            (self.description_widget, theme.colors.text_muted),
            (self.error_widget, theme.colors.danger),
        ):
            palette = widget.palette()
            palette.setColor(QPalette.ColorRole.WindowText, QColor(color))
            widget.setPalette(palette)
            widget.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(theme.spacing.xsmall)
        layout.addWidget(self.label_widget)
        layout.addWidget(control)
        layout.addWidget(self.description_widget)
        layout.addWidget(self.error_widget)
        self.setFocusProxy(control)

        self.setLabelText(label)
        self.setDescriptionText(description)
        self.setErrorText(error)

    def labelText(self) -> str:
        """Return the visible field label."""

        return self.label_widget.text()

    def setLabelText(self, text: str) -> None:
        """Set the visible label and its accessible control association."""

        self.label_widget.setText(text)
        self.label_widget.setVisible(bool(text))
        self.label_widget.setBuddy(self.control)
        accessible_name = _plain_label_text(text)
        self.setAccessibleName(accessible_name)
        self.control.setAccessibleName(accessible_name)

    def descriptionText(self) -> str:
        """Return the visible field description."""

        return self.description_widget.text()

    def setDescriptionText(self, text: str) -> None:
        """Set supplementary field guidance."""

        self.description_widget.setText(text)
        self.description_widget.setVisible(bool(text))
        self._update_accessible_description()

    def errorText(self) -> str:
        """Return the current validation feedback text."""

        return self.error_widget.text()

    def setErrorText(self, text: str) -> None:
        """Show or clear caller-provided validation feedback."""

        self.error_widget.setText(text)
        self.error_widget.setVisible(bool(text))
        self.control.setProperty("invalid", bool(text))
        style = self.control.style()
        style.unpolish(self.control)
        style.polish(self.control)
        self.control.update()
        self._update_accessible_description()

    def _update_accessible_description(self) -> None:
        parts = [self.descriptionText()]
        if self.errorText():
            parts.append(f"Error: {self.errorText()}")
        description = " ".join(part for part in parts if part)
        self.setAccessibleDescription(description)
        self.control.setAccessibleDescription(description)


class TextInput(_Field):
    """Labeled QLineEdit composition with native text signals on ``control``."""

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        *,
        label: str = "",
        description: str = "",
        error: str = "",
        placeholder: str = "",
        validator: QValidator | None = None,
        input_mask: str = "",
        completer: QCompleter | None = None,
    ) -> None:
        control = QLineEdit()
        control.setInputMask(input_mask)
        control.setText(text)
        control.setPlaceholderText(placeholder)
        if validator is not None:
            control.setValidator(validator)
        if completer is not None:
            control.setCompleter(completer)
        _style_control(control, "QLineEdit")
        super().__init__(
            control,
            label=label,
            description=description,
            error=error,
            parent=parent,
        )

    @property
    def textChanged(self):  # noqa: N802
        return self.control.textChanged

    @property
    def editingFinished(self):  # noqa: N802
        return self.control.editingFinished

    def text(self) -> str:
        return self.control.text()

    def setText(self, text: str) -> None:
        self.control.setText(text)

    def clear(self) -> None:
        self.control.clear()

    def placeholderText(self) -> str:
        return self.control.placeholderText()

    def setPlaceholderText(self, text: str) -> None:
        self.control.setPlaceholderText(text)

    def validator(self) -> QValidator | None:
        return self.control.validator()

    def setValidator(self, validator: QValidator | None) -> None:
        self.control.setValidator(validator)

    def hasAcceptableInput(self) -> bool:
        return self.control.hasAcceptableInput()

    def inputMask(self) -> str:
        return self.control.inputMask()

    def setInputMask(self, input_mask: str) -> None:
        self.control.setInputMask(input_mask)

    def completer(self) -> QCompleter | None:
        return self.control.completer()

    def setCompleter(self, completer: QCompleter | None) -> None:
        self.control.setCompleter(completer)

    def isReadOnly(self) -> bool:
        return self.control.isReadOnly()

    def setReadOnly(self, read_only: bool) -> None:
        self.control.setReadOnly(read_only)


class NumberInput(_Field):
    """Labeled native integer or decimal spin box."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        kind: NumberKind = "integer",
        value: int | float | None = None,
        minimum: int | float | None = None,
        maximum: int | float | None = None,
        step: int | float | None = None,
        decimals: int = 2,
        label: str = "",
        description: str = "",
        error: str = "",
    ) -> None:
        if kind not in _NUMBER_KINDS:
            choices = ", ".join(_NUMBER_KINDS)
            raise ValueError(f"kind must be one of: {choices}")
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum must not exceed maximum")
        if step is not None and step <= 0:
            raise ValueError("step must be positive")
        if kind == "decimal" and decimals < 0:
            raise ValueError("decimals must not be negative")

        self.kind: NumberKind = kind
        if kind == "integer":
            control: QSpinBox | QDoubleSpinBox = QSpinBox()
            selector = "QSpinBox"
        else:
            control = QDoubleSpinBox()
            control.setDecimals(decimals)
            selector = "QDoubleSpinBox"
        if minimum is not None:
            control.setMinimum(minimum)
        if maximum is not None:
            control.setMaximum(maximum)
        if step is not None:
            control.setSingleStep(step)
        if value is not None:
            control.setValue(value)
        _style_control(control, selector)
        super().__init__(
            control,
            label=label,
            description=description,
            error=error,
            parent=parent,
        )

    @property
    def valueChanged(self):  # noqa: N802
        return self.control.valueChanged

    def value(self) -> int | float:
        return self.control.value()

    def setValue(self, value: int | float) -> None:
        self.control.setValue(value)

    def minimum(self) -> int | float:
        return self.control.minimum()

    def maximum(self) -> int | float:
        return self.control.maximum()

    def setRange(self, minimum: int | float, maximum: int | float) -> None:
        self.control.setRange(minimum, maximum)

    def singleStep(self) -> int | float:
        return self.control.singleStep()

    def setSingleStep(self, step: int | float) -> None:
        self.control.setSingleStep(step)


class SelectInput(_Field):
    """Labeled QComboBox composition using native items, models, and signals."""

    def __init__(
        self,
        items: Iterable[str] = (),
        parent: QWidget | None = None,
        *,
        label: str = "",
        description: str = "",
        error: str = "",
    ) -> None:
        control = QComboBox()
        control.addItems(list(items))
        _style_control(control, "QComboBox")
        super().__init__(
            control,
            label=label,
            description=description,
            error=error,
            parent=parent,
        )

    @property
    def currentIndexChanged(self):  # noqa: N802
        return self.control.currentIndexChanged

    @property
    def currentTextChanged(self):  # noqa: N802
        return self.control.currentTextChanged

    def addItem(self, text: str, user_data: object | None = None) -> None:
        self.control.addItem(text, user_data)

    def addItems(self, texts: Iterable[str]) -> None:
        self.control.addItems(list(texts))

    def count(self) -> int:
        return self.control.count()

    def currentIndex(self) -> int:
        return self.control.currentIndex()

    def setCurrentIndex(self, index: int) -> None:
        self.control.setCurrentIndex(index)

    def currentText(self) -> str:
        return self.control.currentText()

    def model(self) -> QAbstractItemModel:
        return self.control.model()

    def setModel(self, model: QAbstractItemModel) -> None:
        self.control.setModel(model)


class CheckBox(QCheckBox):
    """Theme-typed QCheckBox preserving native checked signals and behavior."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        theme = _current_theme()
        font = QFont(self.font())
        font.setPointSizeF(theme.typography.body_size)
        font.setWeight(QFont.Weight(theme.typography.body_weight))
        self.setFont(font)
        self.setAccessibleName(_plain_label_text(text))

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.colors.text))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme.colors.primary))
        self.setPalette(palette)


class Switch(QCheckBox):
    """Two-state switch appearance with native QCheckBox behavior and signals."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        theme = _current_theme()
        self._track_width = theme.spacing.xxlarge + theme.spacing.xsmall
        self._track_height = theme.spacing.large + theme.spacing.xsmall
        self._track_spacing = theme.spacing.small
        self.setTristate(False)
        self.setAccessibleName(_plain_label_text(text))

        font = QFont(self.font())
        font.setPointSizeF(theme.typography.body_size)
        font.setWeight(QFont.Weight(theme.typography.body_weight))
        self.setFont(font)

    def sizeHint(self) -> QSize:
        text_width = self.fontMetrics().horizontalAdvance(_plain_label_text(self.text()))
        spacing = self._track_spacing if text_width else 0
        return QSize(
            self._track_width + spacing + text_width,
            max(self._track_height, self.fontMetrics().height()),
        )

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def setTristate(self, tristate: bool = True) -> None:
        if tristate:
            raise ValueError("Switch supports two states only")
        super().setTristate(False)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        theme = _current_theme()
        colors = theme.colors
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track_on_left = self.layoutDirection() == Qt.LayoutDirection.LeftToRight
        track_x = 1.0 if track_on_left else self.width() - self._track_width - 1.0
        track_y = (self.height() - self._track_height) / 2.0
        track = QRectF(track_x, track_y, self._track_width, self._track_height)

        if self.isEnabled():
            track_color = QColor(colors.primary if self.isChecked() else colors.border)
            thumb_color = QColor(colors.surface)
            text_color = QColor(colors.text)
        else:
            track_color = QColor(colors.background)
            thumb_color = QColor(colors.surface)
            text_color = QColor(colors.text_muted)

        focus_color = QColor(colors.info if self.hasFocus() else colors.border)
        painter.setPen(QPen(focus_color, 2.0 if self.hasFocus() else 1.0))
        painter.setBrush(track_color)
        radius = self._track_height / 2.0
        painter.drawRoundedRect(track, radius, radius)

        thumb_margin = 3.0
        thumb_size = self._track_height - 2.0 * thumb_margin
        if self.isChecked():
            thumb_x = track.right() - thumb_margin - thumb_size
        else:
            thumb_x = track.left() + thumb_margin
        thumb = QRectF(thumb_x, track.top() + thumb_margin, thumb_size, thumb_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(thumb_color)
        painter.drawEllipse(thumb)

        if self.text():
            if track_on_left:
                text_left = self._track_width + self._track_spacing
                text_width = self.width() - text_left
            else:
                text_left = 0
                text_width = self.width() - self._track_width - self._track_spacing
            painter.setFont(self.font())
            painter.setPen(text_color)
            alignment = Qt.AlignmentFlag.AlignLeft if track_on_left else Qt.AlignmentFlag.AlignRight
            painter.drawText(
                QRectF(text_left, 0, text_width, self.height()),
                Qt.AlignmentFlag.AlignVCenter | alignment | Qt.TextFlag.TextShowMnemonic,
                self.text(),
            )
