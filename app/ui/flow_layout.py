from PyQt6.QtWidgets import QLayout, QSizePolicy
from PyQt6.QtCore import Qt, QRect, QSize, QPoint


class FlowLayout(QLayout):
    """
    A layout that arranges widgets in a left-to-right flow,
    wrapping to the next row when the available width is exceeded.
    Drop-in replacement for QHBoxLayout in any wrapping context.
    """

    def __init__(self, parent=None, h_spacing: int = 10, v_spacing: int = 8):
        super().__init__(parent)
        self._items = []
        self._h_spacing = h_spacing
        self._v_spacing = v_spacing

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self) -> int:
        return self._h_spacing

    def verticalSpacing(self) -> int:
        return self._v_spacing

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(
            margins.left() + margins.right(),
            margins.top() + margins.bottom()
        )
        return size

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        margins = self.contentsMargins()
        effective_rect = rect.adjusted(
            margins.left(), margins.top(),
            -margins.right(), -margins.bottom()
        )
        x = effective_rect.x()
        y = effective_rect.y()
        row_height = 0

        for item in self._items:
            widget = item.widget()
            if widget is None:
                continue

            item_width = item.sizeHint().width()
            item_height = item.sizeHint().height()

            next_x = x + item_width + self._h_spacing

            if next_x - self._h_spacing > effective_rect.right() and row_height > 0:
                x = effective_rect.x()
                y += row_height + self._v_spacing
                next_x = x + item_width + self._h_spacing
                row_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            row_height = max(row_height, item_height)

        return y + row_height - rect.y() + margins.bottom()