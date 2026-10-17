"""Server-owned entry point for the assembled Zorentia application."""

import re
from pathlib import Path

from flask import abort, send_file, redirect
from backend import create_app as create_backend_app

PROJECT_ROOT = Path(__file__).resolve().parent
SCREEN_ROUTES = {'/': 'frontend/features/local_browser_storage/main_loan_list.html'}
FRONTEND_OWNED_BACKEND_ROUTES = set([])
ENTRY_ROUTE = '/'


def _flask_route(route):
    return re.sub(
        r"\{([A-Za-z_][A-Za-z0-9_]*)\}",
        lambda match: "<" + match.group(1) + ">",
        route,
    )


def _project_file(relative_path):
    target = (PROJECT_ROOT / relative_path).resolve()
    if target != PROJECT_ROOT and PROJECT_ROOT not in target.parents:
        raise RuntimeError("frontend_route_path_invalid")
    return target


def create_app(testing=False, config=None):
    app = create_backend_app(testing=testing, config=config)

    @app.get("/static/css/app.css")
    def frontend_css():
        return send_file(
            _project_file("frontend/shared/ui/library.css"),
            mimetype="text/css",
        )

    @app.get("/__frontend_assets/<path:relative_path>")
    def frontend_asset(relative_path):
        normalized = str(relative_path or "").replace("\\", "/")
        if not (normalized.startswith("frontend/features/") or normalized in {"frontend/shared/ui/library.js", "frontend/shared/ui/runtime.js"}) or not normalized.endswith(".js") or ".." in normalized.split("/"):
            abort(404)
        target = _project_file(normalized)
        if not target.is_file():
            abort(404)
        return send_file(target, mimetype="text/javascript")

    for index, (route, relative_path) in enumerate(SCREEN_ROUTES.items()):
        target = _project_file(relative_path)

        def serve_screen(_target=target, **_route_parameters):
            return send_file(_target, mimetype="text/html")

        flask_route = _flask_route(route)
        existing = next((rule for rule in app.url_map.iter_rules() if rule.rule == flask_route and "GET" in rule.methods), None)
        if existing and route in FRONTEND_OWNED_BACKEND_ROUTES:
            if set(existing.methods) - {"GET", "HEAD", "OPTIONS"}:
                raise RuntimeError("frontend_backend_route_collision")
            app.view_functions[existing.endpoint] = serve_screen
        elif existing:
            raise RuntimeError("frontend_backend_route_collision")
        else:
            app.add_url_rule(
                flask_route,
                endpoint="frontend_screen_" + str(index),
                view_func=serve_screen,
                methods=["GET"],
            )
    if ENTRY_ROUTE and '/' not in SCREEN_ROUTES and not any(rule.rule == '/' and 'GET' in rule.methods for rule in app.url_map.iter_rules()):
        app.add_url_rule('/', endpoint='frontend_entry', view_func=lambda: redirect(ENTRY_ROUTE), methods=['GET'])
    return app
