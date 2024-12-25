from fasthtml.common import FastHTML, serve, Script, H1, H2, Div, Button, Link, A
from charts.common import COMMON_MARGIN
from charts.scatterplot import scatterplot
from charts.barchart import barchart
from charts.rankings import rankings

alpine = Script(src="//unpkg.com/alpinejs", defer=True)

d3 = Script(src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.js", defer=False)

polyfill = Script(src="assets/polyfill.js")
htmx = Script(src="https://unpkg.com/htmx.org@1.9.12/dist/htmx.js")
basestyle = Link(rel="stylesheet", href="assets/styles.css", type="text/css")
gridstyle = Link(rel="stylesheet", href="assets/grid.css", type="text/css")
cardstyle = Link(rel="stylesheet", href="assets/card.css", type="text/css")
rankingstyle = Link(rel="stylesheet", href="assets/RankingFilters.css", type="text/css")
app = FastHTML(
    hdrs=(
        htmx,
        alpine,
        d3,
        polyfill,
        basestyle,
        gridstyle,
        cardstyle,
        rankingstyle,
    ),
    htmx=False,
)

app.static_route(ext="", prefix="/assets", static_path="./static")


ranking_fs = [
    {"id": "satisfaction", "label": "Satisfaction"},
    {"id": "interest", "label": "Interest"},
    {"id": "usage", "label": "Usage"},
    {"id": "awareness", "label": "Awareness"},
]

initial_active = "satisfaction"


def button(label, id, active):
    interior_data = f"framework: '{id}'"
    data = "{" + interior_data + "}"
    return Button(
        label,
        cls="button",
        **{
            "x-data": data,
            ":class": "$store.frameworks.selected == framework && 'active'",
            "@click": '$store.frameworks.previous = $store.frameworks.selected; $store.frameworks.selected =framework; document.querySelectorAll(".path-animation").forEach((e) => e.beginElement());',
        },
    )


def ranking_filters():
    buttons = [
        (
            button(rf["label"], rf["id"], False)
            if rf["id"] != initial_active
            else button(rf["label"], rf["id"], True)
        )
        for rf in ranking_fs
    ]
    return Div(*buttons, rankings(COMMON_MARGIN), cls="ranking-filters")


@app.get("/")
def home():
    return (
        Div(
            Div(
                H1("Front-end Frameworks"),
                Div(
                    (
                        Div(
                            Div(
                                (H2("Rankings"), ranking_filters()),
                                id="rankings",
                                cls="card",
                            ),
                            cls="col-9",
                        ),
                        Div(
                            Div(
                                Div(
                                    Div(
                                        (
                                            H2("Retention vs Usage"),
                                            scatterplot(COMMON_MARGIN),
                                        ),
                                        id="scatterplot",
                                        cls="card",
                                    ),
                                    cls="col-12",
                                ),
                                Div(
                                    Div(
                                        (H2("Awareness"), barchart(COMMON_MARGIN)),
                                        id="barchart",
                                        cls="card",
                                    ),
                                    cls="col-12",
                                ),
                                cls="row",
                            ),
                            cls="col-3",
                        ),
                    ),
                    cls="row",
                ),
                Div(
                    "Data source and original rankings chart: ",
                    A(
                        "The State of JS 2021: Front-end Frameworks",
                        href="https://2021.stateofjs.com/en-US/libraries/front-end-frameworks",
                    ),
                    cls="source",
                ),
                cls="container",
            ),
            id="root",
        ),
        Script(src="assets/charts.js"),
    )


serve()
