import os

# USE CDN for now
os.environ["BOKEH_RESOURCES"] = "cdn"


from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.server.asgi import BokehASGI

from litestar import Litestar, asgi, get
from litestar.types import Receive, Scope, Send

MOUNT = "/bokeh"

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
    # Litestar at mount cuts off  trailing slash (/ws/).
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
