from typing import Dict
from fasthtml.svg import Circle, transformd, G, Line, Text
from fasthtml.common import Template
from .common import chart_container


def scatterplot(margin: Dict[str, int]):
    width = 300
    height = 245
    innerWidth = width - margin["left"] - margin["right"]
    innerHeight = height - margin["top"] - margin["bottom"]
    return chart_container(
        G(
            G(
                Text(
                    transformd(translate=(innerWidth / 2, 42)),
                    text_anchor="middle",
                    **{"x-text": "xlabel"},
                ),
                Line(x1=0, y1=0, x2=innerWidth, y2=0),
                Template(
                    G(
                        Line(x1=0, y1=0, x2=0, y2=5),
                        Text(x=0, y=20, text_anchor="middle", **{"x-text": "t"}),
                        **{"x-bind:transform": "`translate(${xScale(t)},0)`"},
                    ),
                    **{"x-for": "t in xticks"},
                ),
                transformd(translate=(0, innerHeight)),
                cls="axis",
            ),
            G(
                Text(
                    transformd(translate=(-42, innerHeight / 2), rotate=(270,)),
                    text_anchor="middle",
                    **{"x-text": "ylabel"},
                ),
                Line(x1=0, y1=innerHeight, x2=0, y2=0),
                Template(
                    G(
                        Line(x1=-5, y1=0, x2=0, y2=0),
                        Text(
                            x=-10,
                            y=0,
                            text_anchor="end",
                            dominant_baseline="middle",
                            **{"x-text": "t"},
                        ),
                        **{"x-bind:transform": "`translate(0,${yScale(t)})`"},
                    ),
                    **{"x-for": "t in yticks"},
                ),
                cls="axis",
            ),
            Template(
                Circle(
                    r=6,
                    **{
                        "x-bind:cx": "c.x",
                        "x-bind:cy": "c.y",
                        "x-bind:fill": "c.f",
                    },
                ),
                **{"x-for": "c in  circles"},
            ),
            transformd(translate=(margin["left"], margin["top"])),
        ),
        width=width,
        height=height,
        **{
            "x-data": f"scatterplot({innerWidth}, {innerHeight})",
            "x-init": "$watch('$store.frameworks.data', value => render(value))",
        },
    )
