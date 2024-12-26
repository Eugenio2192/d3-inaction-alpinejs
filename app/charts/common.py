from fasthtml.svg import Svg
from typing import Any, Union


def chart_container(
    content: Any,
    width: Union[int, float],
    height: Union[int, float],
    **kwargs,
):
    return Svg(
        content,
        viewBox=f"0 0 {width} {height}",
        width="100%",
        height="100%",
        **kwargs,
    )


COMMON_MARGIN = {"top": 30, "right": 10, "bottom": 50, "left": 60}
