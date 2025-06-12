import pynvim


@pynvim.plugin
class LiveShare(object):

    def __init__(self, nvim) -> None:
        self.nvim = nvim

    @pynvim.autocmd("BufEnter", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_buf_enter(self, filename: str):
        self.nvim.out_write("testplugin is in " + filename + "\n")

    @pynvim.autocmd("TextChanged,TextChangedI", pattern="*.py", sync=True)
    def on_buffer_change(self):
        # Get current buffer number
        buf = self.nvim.current.buffer
        # Get the whole buffer content as a list of lines
        lines = buf[:]
        # Join lines to get full text
        text = "\n".join(lines)

        # For testing, print the length of the buffer
        self.nvim.out_write(f"Buffer changed! Length: {len(text)}\n")
