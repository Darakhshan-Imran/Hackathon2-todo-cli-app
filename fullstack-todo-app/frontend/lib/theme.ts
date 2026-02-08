"use client";

import { createTheme, type ThemeOptions } from "@mui/material/styles";

const commonOptions: ThemeOptions = {
  typography: {
    fontFamily: "Inter, system-ui, -apple-system, sans-serif",
    button: {
      textTransform: "none",
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
  },
};

export const lightTheme = createTheme({
  ...commonOptions,
  palette: {
    mode: "light",
    primary: {
      main: "#dc4c3e",
      light: "#e8756a",
      dark: "#b03d32",
    },
    secondary: {
      main: "#246fe0",
      light: "#5b92e8",
      dark: "#1a56b0",
    },
    background: {
      default: "#fafafa",
      paper: "#ffffff",
    },
    text: {
      primary: "#1a1a1a",
      secondary: "#666666",
    },
    error: {
      main: "#d1453b",
    },
    warning: {
      main: "#eb8909",
    },
    success: {
      main: "#058527",
    },
    info: {
      main: "#246fe0",
    },
    divider: "#e0e0e0",
  },
});

export const darkTheme = createTheme({
  ...commonOptions,
  palette: {
    mode: "dark",
    primary: {
      main: "#de4c4a",
      light: "#e8756a",
      dark: "#b03d32",
    },
    secondary: {
      main: "#4b8cee",
      light: "#7aabf3",
      dark: "#246fe0",
    },
    background: {
      default: "#1e1e1e",
      paper: "#282828",
    },
    text: {
      primary: "#e8e8e8",
      secondary: "#a0a0a0",
    },
    error: {
      main: "#ff6b6b",
    },
    warning: {
      main: "#f5a623",
    },
    success: {
      main: "#4caf50",
    },
    info: {
      main: "#4b8cee",
    },
    divider: "#3d3d3d",
  },
});

export const priorityColors = {
  high: "#d1453b",
  medium: "#eb8909",
  low: "#246fe0",
} as const;

export const statusColors = {
  completed: "#058527",
  in_progress: "#246fe0",
  pending: "#808080",
} as const;
