local function attach_buffer(bufnr)
	local chan_id = vim.fn["LiveShareGetChannelId"]()
	vim.api.nvim_buf_attach(bufnr, false, {
		on_lines = function(...)
			vim.notify("Got into attach")
			vim.fn.rpcnotify(chan_id, "handle_change", ...)
		end,
		on_detach = function(buf)
			vim.fn.rpcnotify(chan_id, "handle_detach", buf)
		end,
	})
end

vim.api.nvim_create_autocmd("BufEnter", {
	pattern = "*.py",
	callback = function(args)
		vim.notify("Enter buffer")
		attach_buffer(args.buf)
	end,
})
