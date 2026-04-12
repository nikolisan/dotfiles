-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local function map(mode, keybind, command, opts)
  if not opts then
    opts = { noremap = true }
  end
  vim.api.nvim_set_keymap(mode, keybind, command, opts)
end

map("i", "jj", "<Esc>")
-- vim.api.nvim_set_keymap("i", "jj", "<Esc>", { noremap = false })
vim.api.nvim_set_keymap("n", "C-Z", ":u", { desc = "Editor undo", noremap = false })

-- vim.keymap.set("n", "<leader>fs", function()
--   require("telescope.builtin").grep_string({ search = vim.fn.input("Grep String > ") })
-- end, { desc = "Grep string search" })
