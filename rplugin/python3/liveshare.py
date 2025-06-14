import pynvim


@pynvim.plugin
class LiveShare(object):

    def __init__(self, nvim) -> None:
        self.nvim = nvim
        self.owner = False
        self.attached = False
        self.nvim.out_write("LiveShare plugin loaded\n")

    @pynvim.rpc_export("handle_change")
    def on_lines(self, *args):
        event, buf, changed_tick, firstline, lastline, new_lastline, bytecount = args
        self.nvim.out_write(
            f"[on_lines] buf={buf}, changed_tick={changed_tick}, "
            f"firstline={firstline}, lastline={lastline}, new_lastline={new_lastline}, "
            f"line={event} bytes={bytecount}\n"
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
        self.nvim.out_write("Started server\n")

    @pynvim.command("StopServer", nargs="*")
    def stop_server(self, args):
        self.attached = False
        self.nvim.out_write(f"Stopped server\n")

    @pynvim.command("JoinSession", nargs="*")
    def join_session(self, args):
        self.nvim.out_write(f"Joining session witha args {args}\n")

    @pynvim.autocmd("BufEnter", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_buf_enter(self, filename: str):
        self.nvim.out_write("testplugin is in " + filename + "\n")

    @pynvim.function("LiveShareGetChannelId", sync=True)
    def get_channel_id(self, args):
        self.nvim.out_write(f"Channel id: {self.nvim.channel_id}\n")
        return self.nvim.channel_id
