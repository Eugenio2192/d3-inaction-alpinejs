from typing import Dict
from fasthtml.svg import transformd, G, Line, Text, Rect, Template
from .common import chart_container


def barchart(margin: Dict[str, int]):
    width = 300
    height = 245
    marginBottom = 85
    innerWidth = width - margin["left"] - margin["right"]
    innerHeight = height - margin["top"] - marginBottom
    return chart_container(
        G(
            G(
                Line(x1=0, y1=0, x2=innerWidth, y2=0),
                Template(
                    G(
                        Text(
                            text_anchor="end",
                            alignment_baseline="middle",
                            **{
                                "x-text": "t[1]",
                                "x-bind:transform": "`translate(${xScale(t[0]) + xScale.bandwidth() / 2}, 8) rotate(-90)`",
                            },
                        )
                    ),
                    **{"x-for": "t in xtickMap"},
                ),
                transformd(translate=(0, innerHeight)),
                cls="axis",
            ),
            G(
                Line(x1=0, y1=0, x2=0, y2=innerHeight),
                Template(
                    G(
                        Line(x1=-5, x2=0, y1=0, y2=0),
                        Text(
                            x=-10,
                            y=0,
                            text_anchor="end",
                            alignment_baseline="middle",
                            x_text="t",
                        ),
                        **{"x-bind:transform": "`translate(0, ${yScale(t)})`"},
                    ),
                    x_for="t in yticks",
                ),
            ),
            G(
                Template(
                    Rect(
                        0,
                        0,
                        **{
                            "x-bind:x": "bar.x",
                            "x-bind:y": "bar.y",
                            "x-bind:width": "bar.width",
                            "x-bind:height": "bar.height",
                            "x-bind:fill": "bar.fill",
                        },
                    ),
                    **{"x-for": "bar in bars"},
                )
            ),
            transformd(translate=(margin["left"], margin["top"])),
        ),
        width=width,
        height=height,
        **{
            "x-data": f"barchart({innerWidth}, {innerHeight})",
            "x-init": "$watch('$store.frameworks.data', value => render(value))",
            # "x-init": '$nextTick(() => {render($store.frameworks.data);})',
        },
    )
