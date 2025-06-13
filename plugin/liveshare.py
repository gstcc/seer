import pynvim


@pynvim.plugin
class LiveShare(object):

    def __init__(self, nvim) -> None:
        self.nvim = nvim

    @pynvim.command("StartServer", nargs="*")
    def start_server(self, args):
        self.nvim.out_write(f"Started server\n")

    @pynvim.command("StopServer", nargs="*")
    def stop_server(self, args):
        self.nvim.out_write(f"Stopped server\n")

    @pynvim.command("JoinSession", nargs="*")
    def join_session(self, args):
        self.nvim.out_write(f"Joining session witha args {args}\n")

    @pynvim.autocmd("BufEnter", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_buf_enter(self, filename: str):
        self.nvim.out_write("testplugin is in " + filename + "\n")

    @pynvim.autocmd("TextChanged,TextChangedI", pattern="*", sync=True)
    def on_buffer_change(self):
        # Get current buffer number
        buf = self.nvim.current.buffer
        # Get the whole buffer content as a list of lines
        lines = buf[:]
        # Join lines to get full text
        text = "\n".join(lines)

        # For testing, print the length of the buffer
        self.nvim.out_write(f"Buffer changed! Length: {len(text)}\n")
