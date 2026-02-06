"use client";

import { useState } from "react";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import { AuthGuard } from "@/components/auth/AuthGuard";
import { Header } from "@/components/layout/Header";
import { Sidebar, SIDEBAR_WIDTH } from "@/components/layout/Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const theme = useTheme();
  const isDesktop = useMediaQuery(theme.breakpoints.up("md"));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <AuthGuard>
      <Box sx={{ display: "flex", minHeight: "100vh" }}>
        <Header
          onMenuClick={handleDrawerToggle}
          showMenuButton
        />

        {/* Desktop: permanent drawer */}
        {isDesktop && (
          <Sidebar
            open
            onClose={() => {}}
            variant="permanent"
          />
        )}

        {/* Mobile: temporary drawer */}
        {!isDesktop && (
          <Sidebar
            open={mobileOpen}
            onClose={handleDrawerToggle}
            variant="temporary"
          />
        )}

        <Box
          component="main"
          sx={{
            flexGrow: 1,
            width: { md: `calc(100% - ${SIDEBAR_WIDTH}px)` },
          }}
        >
          <Toolbar />
          <Box sx={{ p: { xs: 2, sm: 3 } }}>
            {children}
          </Box>
        </Box>
      </Box>
    </AuthGuard>
  );
}
