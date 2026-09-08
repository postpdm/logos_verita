import os

# USE CDN for now
os.environ["BOKEH_RESOURCES"] = "cdn"


from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.server.asgi import BokehASGI

from litestar import Litestar, asgi, get

# make graph
def make_document(doc):
    source = ColumnDataSource(
        data={
            "x": [1, 2, 3, 4, 5],
            "y": [1, 4, 2, 5, 3],
        }
    )

    plot = figure(
        title="Bokeh + Litestar",
        width=800,
        height=500,
        sizing_mode="stretch_width",
    )

    plot.line(
        x="x",
        y="y",
        source=source,
        line_width=3,
    )

    doc.add_root(plot)


# Bokeh-app
bokeh_application = Application(
    FunctionHandler(make_document)
)

# BokehASGI mapping URL -> Application
bokeh_asgi = BokehASGI(
    {
        "/": bokeh_application,
    },
    extra_websocket_origins=[
        "127.0.0.1:8000",
        "localhost:8000",
    ],
)


# Start Bokeh core
async def start_bokeh() -> None:
    await bokeh_asgi.core.start()

# Stop Bokeh core
async def stop_bokeh() -> None:
    await bokeh_asgi.core.stop()

# main Litestar app
@get("/")
async def index() -> dict[str, str]:
    return {
        "message": "Go http://127.0.0.1:8000/bokeh/",
    }


# Mount
bokeh_route = asgi(
    path="/bokeh",
    is_mount=True,
)(bokeh_asgi)


app = Litestar(
    route_handlers=[
        index,
        bokeh_route,
    ],
    on_startup=[
        start_bokeh,
    ],
    on_shutdown=[
        stop_bokeh,
    ],
)
