import os

# USE CDN for now
os.environ["BOKEH_RESOURCES"] = "cdn"


from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.asgi import BokehASGI
from bokeh.layouts import column

from litestar import Litestar, asgi, get
from litestar.types import Receive, Scope, Send

import random

MOUNT = "/bokeh"

# make graph
def make_document(doc):
    # Initial number of points
    initial_n = 50

    def generate_data(n):
        """Generate n random points (x = 0..n-1, y = random values from 0 to 10)."""
        x = list(range(n))
        y = [random.random() * 10 for _ in range(n)]
        return dict(x=x, y=y)

    # Create a data source with initial values
    source = ColumnDataSource(data=generate_data(initial_n))

    # Create the plot
    plot = figure(
        title="Bokeh + Litestar (dynamic random points)",
        #width=800,
        height=500,
        sizing_mode="stretch_width",
    )

    # Line connecting the points
    plot.line(
        x="x",
        y="y",
        source=source,
        line_width=2,
        color="navy",
        alpha=0.8,
    )

    # Slider for choosing the number of points
    slider = Slider(
        start=10,
        end=100,
        value=initial_n,
        step=1,
        title="Number of random points",
    )

    # Callback that fires when the slider value changes
    def update_points(attr, old, new):
        source.data = generate_data(new)

    slider.on_change("value", update_points)

    # Arrange slider and plot vertically
    layout = column(slider, plot, sizing_mode="stretch_width")

    # Add the layout to the Bokeh document
    doc.add_root(layout)

# BokehASGI mapping URL -> Application
bokeh_asgi = BokehASGI(
    make_document,
    
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
@asgi(path=MOUNT, is_mount=True, copy_scope=True)
async def bokeh_route(scope: Scope, receive: Receive, send: Send) -> None:
    # Litestar at mount cuts off trailing slash (/ws/).
    # BokehASGI want for /ws and root_path.
    if scope["type"] in ("http", "websocket"):
        scope = dict(scope)
        path = scope.get("path", "/")
        if len(path) > 1 and path.endswith("/"):
            scope["path"] = path.rstrip("/") or "/"

        existing = scope.get("root_path", "") or ""
        mount = MOUNT.rstrip("/")
        if mount and not existing.rstrip("/").endswith(mount):
            scope["root_path"] = existing.rstrip("/") + mount

    await bokeh_asgi(scope, receive, send)


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
