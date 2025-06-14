from .connector import Connector
import pynvim
import asyncio
import json


@pynvim.plugin
class LiveShare(object):

    class LiveShareConnector(Connector):
        def __init__(self, user: str, host: str, port: int, owner: bool, nvim, buffer):
            super().__init__(user, host, port)
            self.owner = owner
            self.nvim = nvim
            self.buffer = buffer

        async def on_message(self, message):
            data = json.loads(message)

            if data.get("type") == "update":
                new_lines = data["content"].split("\n")

                # Safely update buffer in Neovim main loop
                self.nvim.async_call(self.update_buffer, new_lines)

        def update_buffer(self, new_lines):
            try:
                # Replace entire buffer content
                self.buffer[:] = new_lines
                self.nvim.out_write("[LiveShare] Buffer updated from server.\n")
            except Exception as e:
                self.nvim.err_write(f"[LiveShare] Failed to update buffer: {e}\n")

    def __init__(self, nvim) -> None:
        self.nvim = nvim
        self.owner: bool = False
        self.attached: bool = False
        self.nvim.out_write("LiveShare plugin loaded\n")
        self.connector = None

    @pynvim.rpc_export("handle_change")
    def on_lines(self, *args):
        event, buf, changed_tick, firstline, lastline, new_lastline, bytecount = args

        old_lines = self.nvim.api.buf_get_lines(buf, firstline, lastline, False)

        # Log the change
        self.nvim.out_write(
            f"[on_lines] changed_tick={changed_tick}, "
            f"firstline={firstline}, lastline={lastline}, new_lastline={new_lastline}, "
            f"old_lines={old_lines}\n"
        )

    @pynvim.rpc_export("handle_detach")
    def on_detach(self, buf):
        self.nvim.out_write(f"[on_detach] Buffer {buf} detached\n")
        self.attached = False

    @pynvim.command("StartServer", nargs="*")
    def start_server(self, args):
        if self.attached:
            self.nvim.out_write("Already watching buffer\n")
            return
        self.attached = True
        # self.nvim.out_write(f"Started server, " f"Buffer={self.nvim.current.buffer}\n")

    @pynvim.command("StopServer", nargs="*")
    def stop_server(self, args):
        self.attached = False
        self.nvim.out_write(f"Stopped server\n")

    @pynvim.command("JoinSession", nargs="*")
    def join_session(self, args):
        # Example: assume first arg is user, second host, third port
        user, host, port = args[0], args[1], int(args[2])
        buf = self.nvim.current.buffer

        self.connector = self.LiveShareConnector(
            user, host, port, owner=self.owner, nvim=self.nvim, buffer=buf
        )
        asyncio.create_task(self.connector.join_session())

    @pynvim.autocmd("BufEnter", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_buf_enter(self, filename: str):
        self.nvim.out_write("testplugin is in " + filename + "\n")

    @pynvim.function("LiveShareGetChannelId", sync=True)
    def get_channel_id(self, args):
        self.nvim.out_write(f"Channel id: {self.nvim.channel_id}\n")
        return self.nvim.channel_id

    def apply_diff(self, buffer, lines):
        pass
