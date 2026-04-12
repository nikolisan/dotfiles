return {
  {
    "shaunsingh/nord.nvim",
    lazy = false,
    priority = 1000,
    config = function()
      vim.g.nord_contrast = true
      vim.g.nord_borders = false
      vim.g.nord_disable_background = true
      vim.g.nord_italic = true
      vim.cmd.colorscheme("nord")
      vim.api.nvim_set_hl(0, "WinBar", { bg = "#2e3440", fg = "#eceff4" })
      vim.api.nvim_set_hl(0, "WinBarNC", { bg = "#2e3440", fg = "#4c566a" })
      vim.api.nvim_set_hl(0, "SnacksExplorerNormal", { fg = "#eceff4" })
      vim.api.nvim_set_hl(0, "SnacksExplorerDir", { fg = "#88c0d0", bold = true })
      vim.api.nvim_set_hl(0, "SnacksExplorerFile", { fg = "#eceff4" })
    end,
  },
}
