from typing import Dict
from fasthtml.svg import Circle, transformd, G, Line, Text, ft_svg
from fasthtml.common import Template
from .common import chart_container


def rankings(margin: Dict[str, int]):
    width = 1000
    height = 542
    marginRight = 150
    marginLeft = 110
    innerWidth = width - marginLeft - marginRight
    innerHeight = height - margin["top"] - margin["bottom"]
    dur = "0.25s"
    return chart_container(
        G(
            Template(
                G(
                    Line(x1=0, y1=innerHeight, x2=0, y2=0, stroke_Dasharray="6 4"),
                    Text(x=0, y=innerHeight + 40, text_anchor="middle", x_text="year"),
                    cls="axis",
                    **{
                        "x-bind:key": "`line-year-${year}`",
                        "x-bind:transform": "`translate(${xScale(year)}, 0)`",
                    },
                ),
                **{"x-for": "year in years"},
            ),
            G(
                Template(
                    G(
                        ft_svg(
                            "path",
                            d="",
                            cls="fmwk-curve",
                            stroke_width=5,
                            fill="none",
                            **{
                                "x-bind:id": "`path-curve-${framework.id}`",
                                "x-bind:stroke": "$store.frameworks.colorScale(framework.id)",
                                "x-init":"updateCurve($el,framework[$store.frameworks.selected]);$watch('framework[$store.frameworks.selected]', (data) => updateCurve($el,data))",
                            },
                        ),
                        Template(
                            G(Text(
                                x=0,y=0,
                                text_anchor="end",
                                alignment_baseline="middle",
                                font_weight="bold",
                                **{
                                    "x-text": "framework.name",
                                    "x-bind:fill": "$store.frameworks.colorScale(framework.id)",
                                },
                            ),
                            cls="label",
                            **{"x-bind:style": "`transform: translate(-25px, ${yScale(framework[$store.frameworks.selected][0].rank)}px)`"}
                            ),
                            **{"x-if": "framework[$store.frameworks.selected][0].rank"},
                        ),
                        G(Text(
                            x=0,
                            y=0,
                            text_anchor="start",
                            alignment_baseline="middle",
                            font_weight="bold",
                            **{
                                "x-text": "framework.name",
                                # "x-bind:x": "width + 25",
                                # "x-bind:y": "yScale(framework[$store.frameworks.selected][framework[$store.frameworks.selected].length - 1].rank)",
                                "x-bind:fill": "$store.frameworks.colorScale(framework.id)",
                            },
                        ),
                            cls="label",
                            **{"x-bind:style": "`transform: translate(${width + 25}px, ${yScale(framework[$store.frameworks.selected][framework[$store.frameworks.selected].length - 1].rank)}px)`"}
                        ),
                        Template(
                            Template(
                                ft_svg(
                                    "g",
                                    Circle(
                                        fill="white",
                                        r="18px",
                                        stroke_width="3px",
                                        **{
                                            "x-bind:stroke": "$store.frameworks.colorScale(framework.id)"
                                        },
                                    ),
                                    Text(
                                        x_text='Math.round(entry.percentage_question) + "%"',
                                        text_anchor="middle",
                                        alignment_baseline="middle",
                                        fill="#374f5e",
                                        font_size="12px",
                                    ),
                                    cls="label",
                                    **{
                                        "x-bind:transform": "`translate(${xScale(entry.year)}, ${yScale(entry.rank)})`",
                                        "x-bind:id": "`badge-${entry.rank}-{entry.year}`",
                                    },
                                ),
                                x_if="entry.rank",
                            ),
                            **{
                                "x-for": "(entry, index) in framework[$store.frameworks.selected]"
                            },
                        ),
                        **{"x-bind:key": "`curve-${framework.id}`"},
                    ),
                    **{"x-for": "framework in data"},
                )
            ),
            transformd(translate=(marginLeft, margin["top"])),
        ),
        width=width,
        height=height,
        **{
            "x-data": f"rankings({innerWidth}, {innerHeight})",
            "x-init": "$watch('$store.frameworks.data', (value) => {render(value);} );",
        },
    )
