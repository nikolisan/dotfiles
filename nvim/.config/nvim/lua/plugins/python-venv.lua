return {
  "linux-cultist/venv-selector.nvim",
  cmd = "VenvSelect",
  enabled = function()
    return LazyVim.has("telescope.nvim")
  end,
  opts = {
    settings = {
      options = {
        notify_user_on_venv_activation = true,
      },
    },
  },
  ft = "python",
  keys = { { "<leader>cv", "<cmd>:VenvSelect<cr>", desc = "Select Virtual Env", ft = "python" } },
}
