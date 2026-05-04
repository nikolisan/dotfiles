-- return {
--   {
--     "uZer/pywal16.nvim",
--     -- for local dev replace with:
--     -- dir = '~/your/path/pywal16.nvim',
--     config = function()
--       vim.cmd.colorscheme("pywal16")
--     end,
--   },
-- }

return {
  "RedsXDD/neopywal.nvim",
  enabled = false,
  lazy = false,
  config = function()
    vim.cmd.colorscheme("neopywal") -- activate the colorscheme
  end,
  priority = 1000, -- recommended to ensure the colorscheme
  -- is loaded before other plugins
}
