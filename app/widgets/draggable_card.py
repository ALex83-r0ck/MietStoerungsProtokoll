from kivy.properties import BooleanProperty
from kivymd.uix.card import MDCard


class MyDraggableCard(MDCard):
    """
    Custom draggable card widget that allows the user to drag the card within a specific area.
    """

    dragging = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
        Initialize the draggable card with touch offset values.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self._touch_offset_x = 0
        self._touch_offset_y = 0

    def on_touch_down(self, touch):
        """
        Handle touch down event to start dragging the card if the touch is within the draggable area.

        Args:
            touch: Touch event object.

        Returns:
            bool: True if the touch event is consumed, False otherwise.
        """
        if self.collide_point(*touch.pos) and touch.pos[1] > self.y + self.height * 0.9:
            self.dragging = True
            self._touch_offset_x = self.x - touch.x
            self._touch_offset_y = self.y - touch.y
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        """
        Handle touch move event to move the card if dragging is enabled.

        Args:
            touch: Touch event object.

        Returns:
            bool: True if the touch event is consumed, False otherwise.
        """
        if self.dragging:
            self.x = touch.x + self._touch_offset_x
            self.y = touch.y + self._touch_offset_y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """
        Handle touch up event to stop dragging when touch is released.

        Args:
            touch: Touch event object.

        Returns:
            bool: True if the touch event is consumed, False otherwise.
        """
        if self.dragging:
            self.dragging = False
            return True
        return super().on_touch_up(touch)
