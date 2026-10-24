"""Generic form components composed from native Qt controls."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from PySide6.QtCore import QAbstractItemModel, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPalette,
    QPen,
    QPolygonF,
    QValidator,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QCompleter,
    QDoubleSpinBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QStyle,
    QStyleOptionButton,
    QStyleOptionSpinBox,
    QVBoxLayout,
    QWidget,
)

from alp_ui.components.actions import Button
from alp_ui.theme.appearance import density_metrics, interactions
from alp_ui.theme.install import _current_theme

NumberKind = Literal["integer", "decimal"]
_NUMBER_KINDS = ("integer", "decimal")


def _plain_label_text(text: str) -> str:
    return text.replace("&&", "\0").replace("&", "").replace("\0", "&")


def _style_control(control: QWidget, selector: str) -> None:
    """Uniform native controls; only subcontrol chrome is locally restyled."""
    theme = _current_theme()
    colors = theme.colors
    state = interactions(theme)
    metrics = density_metrics(theme)
    font = QFont(control.font())
    font.setPointSizeF(theme.typography.body_size)
    font.setWeight(QFont.Weight(theme.typography.body_weight))
    control.setFont(font)
    control.setMinimumHeight(metrics.control_height)

    palette = control.palette()
    for role, value in (
        (QPalette.ColorRole.Base, colors.surface),
        (QPalette.ColorRole.Text, colors.text),
        (QPalette.ColorRole.Button, colors.surface),
        (QPalette.ColorRole.ButtonText, colors.text),
        (QPalette.ColorRole.PlaceholderText, colors.text_muted),
        (QPalette.ColorRole.Highlight, colors.primary),
        (QPalette.ColorRole.HighlightedText, colors.on_primary),
    ):
        palette.setColor(role, QColor(value))
    control.setPalette(palette)

    # All borders stay one pixel in every state: no focus-induced geometry jump.
    stylesheet = f"""
        {selector} {{
            background-color: {colors.surface};
            color: {colors.text};
            border: 1px solid {colors.border};
            border-radius: {theme.radii.button}px;
            padding: 0 {theme.spacing.medium}px;
        }}
        {selector}:hover {{ border-color: {state.border_hover}; }}
        {selector}:focus {{ border-color: {state.focus}; }}
        {selector}[invalid="true"] {{ border-color: {colors.danger}; }}
        {selector}:disabled {{
            background-color: {state.disabled_surface};
            color: {state.disabled_text};
            border-color: {colors.border};
        }}
    """
    if selector == "QComboBox":
        stylesheet += f"""
            QComboBox {{ padding-right: 30px; }}
            QComboBox:right-to-left {{ padding-left: 30px; padding-right: 12px; }}
            QComboBox::drop-down {{ border: 0; width: 28px; background: transparent; }}
            QComboBox::down-arrow {{ image: none; width: 0; height: 0; }}
            QComboBox QAbstractItemView {{
                background: {colors.surface};
                color: {colors.text};
                border: 1px solid {colors.border};
                selection-background-color: {state.selected_surface};
                selection-color: {colors.text};
                outline: 0;
            }}
        """
    elif selector in ("QSpinBox", "QDoubleSpinBox"):
        stylesheet += f"""
            {selector} {{ padding-right: 29px; }}
            {selector}:right-to-left {{ padding-left: 29px; padding-right: 12px; }}
            {selector}::up-button, {selector}::down-button {{
                width: 24px;
                border: 0;
                background: transparent;
            }}
            {selector}::up-button {{ border-left: 1px solid {colors.border}; }}
            {selector}::down-button {{ border-left: 1px solid {colors.border}; }}
            {selector}::up-arrow, {selector}::down-arrow {{
                image: none; width: 0; height: 0;
            }}
        """
    control.setStyleSheet(stylesheet)


def _chevron(painter: QPainter, center: QPointF, *, up: bool, color: QColor) -> None:
    """Original one-stroke glyph used without an icon pack or external assets."""
    pen = QPen(color, 1.6)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    offset = -1 if up else 1
    painter.drawPolyline(
        QPolygonF(
            [
                QPointF(center.x() - 3.5, center.y() - offset * 1.75),
                QPointF(center.x(), center.y() + offset * 1.75),
                QPointF(center.x() + 3.5, center.y() - offset * 1.75),
            ]
        )
    )


class _StyledComboBox(QComboBox):
    """Custom chevron, native QComboBox popup, model, keyboard and accessibility."""

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        state = interactions(_current_theme())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x = 15 if self.layoutDirection() == Qt.LayoutDirection.RightToLeft else self.width() - 15
        color = QColor(
            state.disabled_text if not self.isEnabled() else _current_theme().colors.text_muted
        )
        _chevron(painter, QPointF(x, self.height() / 2), up=False, color=color)


class _SpinChrome:
    """Shared arrow painting; native spin-box buttons still implement stepping."""

    def _paint_arrows(self) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        option = QStyleOptionSpinBox()
        self.initStyleOption(option)
        state = interactions(_current_theme())
        color = QColor(
            state.disabled_text if not self.isEnabled() else _current_theme().colors.text_muted
        )
        for part, up in (
            (QStyle.SubControl.SC_SpinBoxUp, True),
            (QStyle.SubControl.SC_SpinBoxDown, False),
        ):
            rect = self.style().subControlRect(QStyle.ComplexControl.CC_SpinBox, option, part, self)
            if rect.isValid() and not rect.isEmpty():
                _chevron(painter, QPointF(rect.center()), up=up, color=color)


class _StyledSpinBox(_SpinChrome, QSpinBox):
    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        self._paint_arrows()


class _StyledDoubleSpinBox(_SpinChrome, QDoubleSpinBox):
    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        self._paint_arrows()


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
        message_font.setPointSizeF(theme.typography.caption_size)
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


class FolderPicker(QWidget):
    """Read-only folder path display with a native directory selection dialog."""

    folderChanged = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        label: str = "",
    ) -> None:
        super().__init__(parent)
        self._folder_path = ""
        self.label_widget = QLabel(self)
        self.control = QLineEdit(self)
        self.choose_button = Button("Choose folder", self, variant="outline")
        self.choose_button.setAutoDefault(True)

        self.control.setReadOnly(True)
        _style_control(self.control, "QLineEdit")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(_current_theme().spacing.xsmall)
        layout.addWidget(self.label_widget)
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(_current_theme().spacing.small)
        row.addWidget(self.control, 1)
        row.addWidget(self.choose_button)
        layout.addLayout(row)

        self.setLabelText(label)
        self._update_path_accessibility()
        self.setFocusProxy(self.choose_button)
        self.choose_button.clicked.connect(self._choose_folder)

    def labelText(self) -> str:
        """Return the visible label."""

        return self.label_widget.text()

    def setLabelText(self, text: str) -> None:
        """Set the visible label and associated accessible names."""

        self.label_widget.setText(text)
        self.label_widget.setVisible(bool(text))
        self.label_widget.setBuddy(self.control)
        accessible_label = _plain_label_text(text) or "Folder"
        self.setAccessibleName(accessible_label)
        self.control.setAccessibleName(accessible_label)
        self.choose_button.setAccessibleName(
            f"Choose {accessible_label}" if text else "Choose folder"
        )

    def folderPath(self) -> str:
        """Return the selected path, or an empty string when none is selected."""

        return self._folder_path

    def setFolderPath(self, path: str) -> None:
        """Set the selected path without resolving, validating, or reading it."""

        if not isinstance(path, str):
            raise TypeError("path must be a str")
        if path == self._folder_path:
            return
        self._folder_path = path
        self.control.setText(path)
        self._update_path_accessibility()
        self.folderChanged.emit(path)

    def _choose_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            "Choose folder",
            self._folder_path,
            QFileDialog.Option.ShowDirsOnly,
        )
        if path:
            self.setFolderPath(path)

    def _update_path_accessibility(self) -> None:
        description = self._folder_path or "No folder selected"
        self.control.setAccessibleDescription(description)
        self.control.setToolTip(self._folder_path)


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
            control: QSpinBox | QDoubleSpinBox = _StyledSpinBox()
            selector = "QSpinBox"
        else:
            control = _StyledDoubleSpinBox()
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
        control = _StyledComboBox()
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

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        theme = _current_theme()
        state = interactions(theme)
        option = QStyleOptionButton()
        self.initStyleOption(option)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Native text, shortcuts and RTL layout; only the indicator is repainted.
        label_option = QStyleOptionButton(option)
        label_option.rect = self.style().subElementRect(
            QStyle.SubElement.SE_CheckBoxContents, option, self
        )
        self.style().drawControl(
            QStyle.ControlElement.CE_CheckBoxLabel, label_option, painter, self
        )
        rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, option, self)
        rect = QRectF(rect).adjusted(1, 1, -1, -1)
        checked = self.checkState() == Qt.CheckState.Checked
        partial = self.checkState() == Qt.CheckState.PartiallyChecked
        enabled = self.isEnabled()
        background = (
            theme.colors.primary
            if enabled and (checked or partial)
            else state.disabled_surface
            if not enabled
            else state.hover_surface
            if self.underMouse()
            else theme.colors.surface
        )
        outline = (
            state.focus
            if self.hasFocus()
            else (state.border_hover if self.underMouse() and enabled else theme.colors.border)
        )
        painter.setPen(QPen(QColor(outline), 1.4 if self.hasFocus() else 1.0))
        painter.setBrush(QColor(background))
        painter.drawRoundedRect(rect, 4, 4)
        if checked or partial:
            pen = QPen(QColor(theme.colors.on_primary if enabled else state.disabled_text), 1.9)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            center = rect.center()
            if partial:
                painter.drawLine(
                    QPointF(center.x() - 4, center.y()),
                    QPointF(center.x() + 4, center.y()),
                )
            else:
                painter.drawPolyline(
                    QPolygonF(
                        [
                            QPointF(center.x() - 4, center.y()),
                            QPointF(center.x() - 1, center.y() + 3),
                            QPointF(center.x() + 4.5, center.y() - 3),
                        ]
                    )
                )


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
        state = interactions(theme)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track_on_left = self.layoutDirection() == Qt.LayoutDirection.LeftToRight
        track_x = 1.0 if track_on_left else self.width() - self._track_width - 1.0
        track_y = (self.height() - self._track_height) / 2.0
        track = QRectF(track_x, track_y, self._track_width, self._track_height)

        if self.isEnabled():
            track_color = QColor(
                colors.primary
                if self.isChecked()
                else state.border_hover
                if self.underMouse()
                else colors.border
            )
            thumb_color = QColor(colors.surface)
            text_color = QColor(colors.text)
        else:
            track_color = QColor(state.disabled_surface)
            thumb_color = QColor(colors.surface)
            text_color = QColor(state.disabled_text)

        focus_color = QColor(state.focus if self.hasFocus() else colors.border)
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
