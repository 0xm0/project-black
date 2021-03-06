import asyncio


class HostHandlers(object):

    def __init__(self, socketio, scope_manager):
        self.socketio = socketio
        self.scope_manager = scope_manager

        self.register_handlers()

    def register_handlers(self):
        @self.socketio.on('hosts:resolve', namespace='/hosts')
        async def _cb_handle_scope_resolve(sio, msg):
            """ On receive, resolve the needed scope """
            hosts_ids = msg['hosts_ids']
            project_uuid = msg['project_uuid']

            total_ips, new_ips = await self.scope_manager.resolve_scopes(hosts_ids, project_uuid)

            await self.socketio.emit(
                'hosts:resolve:done', {
                    'status': 'success',
                    'project_uuid': project_uuid
                },
                room=sio,
                namespace='/hosts'
            )


class ScopeHandlers(object):
    def __init__(self, socketio, scope_manager):
        self.socketio = socketio
        self.scope_manager = scope_manager

        self.register_handlers()

    def register_handlers(self):
        HostHandlers(self.socketio, self.scope_manager)

        @self.socketio.on('scopes:delete:scope_id', namespace='/scopes')
        async def _cb_handle_scope_delete(sio, msg):
            """ When received this message, delete the scope """
            scope_id = msg['scope_id']
            project_uuid = msg['project_uuid']
            scope_type = msg['scope_type']

            # Delete new scope (and register it)
            delete_result = await self.scope_manager.delete_scope(
                scope_id=scope_id, scope_type=scope_type)

            if delete_result["status"] == "success":
                # Send the success result
                if scope_type == 'ip_address':
                    await self.socketio.emit(
                        'ips:delete', {
                            'status': 'success',
                            '_id': scope_id,
                            'project_uuid': project_uuid
                        },
                        namespace='/ips'
                    )
                else:
                    await self.socketio.emit(
                        'hosts:delete', {
                            'status': 'success',
                            '_id': scope_id,
                            'project_uuid': project_uuid
                        },
                        namespace='/hosts'
                    )
            else:
                # Error occured
                await self.socketio.emit(
                    'scopes:delete', {
                        'status': 'error',
                        'text': delete_result["text"],
                        'project_uuid': project_uuid
                    },
                    room=sio,
                    namespace='/scopes'
                )
