""" Main application, running on sanic """
import os
import base64

import socketio
from sanic import Sanic, response
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from events_handling import Handlers

from common.logger import init_default
from config import CONFIG

from managers.meta_manager import MetaManager

from server.handlers.dictionaries import DictHandlers
from server.handlers.ips import IPsHandlers
from server.handlers.projects import ProjectsHandlers
from server.handlers.static import StaticHandlers
from server.handlers.utils import authorized


if __name__ == '__main__':
    init_default()

    meta_manager = MetaManager()

    socketio = socketio.AsyncServer(async_mode='sanic')
    app = Sanic()

    socketio.attach(app)

    # Manage projects
    projects_handlers = ProjectsHandlers(meta_manager.project_manager, socketio)
    app.add_route(projects_handlers.cb_get_projects, '/projects')
    app.add_route(projects_handlers.cb_create_project, '/projects/create', methods=['POST'])
    app.add_route(projects_handlers.cb_delete_project, '/projects/delete', methods=['POST'])
    app.add_route(projects_handlers.cb_update_project, '/projects/update', methods=['POST'])
    
    # Manager IPS
    ips_handlers = IPsHandlers(meta_manager.scope_manager, socketio)
    app.add_route(ips_handlers.cb_get_ips, '/project/<project_uuid>/ips')

    # Static handlers: index.html and bundle.js
    app.add_route(StaticHandlers.cb_index_handler, '/')
    app.add_route(StaticHandlers.cb_index_handler, '/project/<project_uuid>')
    app.add_route(StaticHandlers.cb_index_handler, '/project/<project_uuid>/dirsearch')
    app.add_route(StaticHandlers.cb_index_handler, '/project/<project_uuid>/host/<host>')
    app.add_route(StaticHandlers.cb_index_handler, '/project/<project_uuid>/ip/<host>')
    app.add_route(StaticHandlers.cb_bundle_handler, '/bundle.js')
    # app.add_route(StaticHandlers.cb_serve_media_file, '/<filename:[a-z0-9]+.(eot|woff|woff2)>')

    dict_handlers = DictHandlers(meta_manager.dict_manager)
    app.add_route(dict_handlers.cb_upload_dict, '/upload_dict', methods=['POST'])
    app.add_route(dict_handlers.cb_get_dictionary, '/dictionary/<dict_id>')

    HANDLERS = Handlers(socketio, app, meta_manager)

    @app.listener('before_server_start')
    async def cb_instantiate_scheduler(app, loop):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(HANDLERS.sender_loop, 'interval', seconds=1)
        scheduler.start()


    app.run(host=CONFIG['application']['host'], port=CONFIG['application']['port'], debug=False)
