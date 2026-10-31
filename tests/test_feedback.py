from __future__ import annotations

from dataclasses import replace

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QProgressBar, QPushButton, QStyle, QWidget

from alp_ui.components import Alert, Badge, EmptyState, ProgressBar
from alp_ui.theme import ALPACA_LIGHT, install_theme


@pytest.fixture(autouse=True)
def _install_default_theme(qapp: QApplication) -> None:
    install_theme(qapp)


@pytest.mark.parametrize("intent", ["neutral", "info", "success", "warning", "danger"])
def test_badge_supports_only_generic_intents_with_accessible_text(intent: str) -> None:
    badge = Badge("Available", intent=intent)  # type: ignore[arg-type]

    assert isinstance(badge, QLabel)
    assert badge.intent == intent
    assert badge.accessibleName() == "Available"
    assert badge.accessibleDescription() == f"{intent.capitalize()} intent"


def test_feedback_rejects_unknown_intent() -> None:
    with pytest.raises(ValueError, match="intent must be one of"):
        Badge("Unknown", intent="running")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="intent must be one of"):
        Alert("Unknown", intent="completed")  # type: ignore[arg-type]


def test_badge_updates_validated_intent_in_place() -> None:
    badge = Badge("Checking", intent="warning")
    original_identity = id(badge)

    badge.setIntent("danger")

    assert id(badge) == original_identity
    assert badge.intent == "danger"
    assert badge.accessibleDescription() == "Danger intent"
    assert ALPACA_LIGHT.colors.danger in badge.styleSheet()
    assert ALPACA_LIGHT.colors.warning not in badge.styleSheet()

    with pytest.raises(ValueError, match="intent must be one of"):
        badge.setIntent("completed")  # type: ignore[arg-type]

    assert badge.intent == "danger"
    assert badge.accessibleDescription() == "Danger intent"
    assert ALPACA_LIGHT.colors.danger in badge.styleSheet()


def test_alert_wraps_text_and_owns_consumer_action() -> None:
    parent = QWidget()
    action = QPushButton("Retry")
    alert = Alert(
        "The operation could not be completed. Try again when the connection returns.",
        parent,
        title="Connection unavailable",
        intent="danger",
        action=action,
    )

    assert alert.parent() is parent
    assert action.parent() is alert
    assert alert.title_widget.wordWrap()
    assert alert.text_widget.wordWrap()
    assert alert.accessibleName() == "Danger alert: Connection unavailable"
    assert alert.accessibleDescription().startswith("The operation")
    assert ALPACA_LIGHT.colors.danger in alert.styleSheet()


def test_progress_bar_preserves_native_range_and_indeterminate_modes() -> None:
    determinate = ProgressBar(minimum=0, maximum=200, value=75)
    indeterminate = ProgressBar(minimum=0, maximum=0)

    assert isinstance(determinate, QProgressBar)
    assert (determinate.minimum(), determinate.maximum(), determinate.value()) == (0, 200, 75)
    determinate.setValue(250)
    assert determinate.value() == 75
    assert (indeterminate.minimum(), indeterminate.maximum()) == (0, 0)
    assert indeterminate.accessibleName() == "Progress"
    assert ALPACA_LIGHT.colors.primary in determinate.styleSheet()


def test_empty_state_owns_optional_icon_and_action(qapp: QApplication) -> None:
    action = QPushButton("Add item")
    icon = qapp.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView)
    state = EmptyState(
        "Nothing here yet",
        text="Add an item to get started.",
        icon=icon,
        action=action,
    )

    assert action.parent() is state
    assert state.icon_widget.pixmap() is not None
    assert state.title_widget.wordWrap()
    assert state.text_widget.wordWrap()
    assert state.accessibleName() == "Nothing here yet"
    assert state.accessibleDescription() == "Add an item to get started."


def test_feedback_uses_installed_theme_tokens(qapp: QApplication) -> None:
    custom = replace(
        ALPACA_LIGHT,
        colors=replace(ALPACA_LIGHT.colors, success="#166534", surface="#FEFEFE"),
    )
    install_theme(qapp, custom)

    badge = Badge("Ready", intent="success")
    alert = Alert("Ready to continue", intent="success")

    assert custom.colors.success in badge.styleSheet()
    assert custom.colors.success in alert.styleSheet()
    assert ALPACA_LIGHT.colors.success not in badge.styleSheet()
