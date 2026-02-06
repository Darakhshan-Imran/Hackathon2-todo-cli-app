"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import AddIcon from "@mui/icons-material/Add";
import InboxIcon from "@mui/icons-material/Inbox";
import TodayIcon from "@mui/icons-material/Today";
import UpcomingIcon from "@mui/icons-material/DateRange";
import FlagIcon from "@mui/icons-material/Flag";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";
import PersonIcon from "@mui/icons-material/Person";
import { priorityColors, statusColors } from "@/lib/theme";

export const SIDEBAR_WIDTH = 280;

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  variant: "permanent" | "temporary";
}

export function Sidebar({ open, onClose, variant }: SidebarProps) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const router = useRouter();

  const currentStatus = searchParams.get("status");
  const currentPriority = searchParams.get("priority");
  const currentDue = searchParams.get("due");

  const navigateWithFilter = (params: Record<string, string>) => {
    const sp = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value) sp.set(key, value);
    }
    const query = sp.toString();
    router.push(`/todos${query ? `?${query}` : ""}`);
    if (variant === "temporary") onClose();
  };

  const isActive = (path: string, filterParams?: Record<string, string>) => {
    if (path !== pathname) return false;
    if (!filterParams) return !currentStatus && !currentPriority && !currentDue;
    return Object.entries(filterParams).every(
      ([key, value]) => searchParams.get(key) === value
    );
  };

  const drawerContent = (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <Box sx={{ p: 2 }}>
        <Button
          variant="contained"
          fullWidth
          startIcon={<AddIcon />}
          onClick={() => {
            router.push("/todos/new");
            if (variant === "temporary") onClose();
          }}
          sx={{ py: 1.2 }}
        >
          Add Task
        </Button>
      </Box>

      <List dense>
        <ListItem disablePadding>
          <ListItemButton
            selected={isActive("/todos")}
            onClick={() => navigateWithFilter({})}
          >
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary="All Todos" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            selected={pathname === "/todos" && searchParams.has("due") && searchParams.get("due") === "today"}
            onClick={() => navigateWithFilter({ due: "today" })}
          >
            <ListItemIcon>
              <TodayIcon />
            </ListItemIcon>
            <ListItemText primary="Today" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            selected={pathname === "/todos" && searchParams.has("due") && searchParams.get("due") === "upcoming"}
            onClick={() => navigateWithFilter({ due: "upcoming" })}
          >
            <ListItemIcon>
              <UpcomingIcon />
            </ListItemIcon>
            <ListItemText primary="Upcoming" />
          </ListItemButton>
        </ListItem>
      </List>

      <Divider />

      <Typography variant="overline" sx={{ px: 2, pt: 2, color: "text.secondary" }}>
        Priority
      </Typography>
      <List dense>
        {(["high", "medium", "low"] as const).map((p) => (
          <ListItem key={p} disablePadding>
            <ListItemButton
              selected={isActive("/todos", { priority: p })}
              onClick={() => navigateWithFilter({ priority: p })}
            >
              <ListItemIcon>
                <FlagIcon sx={{ color: priorityColors[p] }} />
              </ListItemIcon>
              <ListItemText
                primary={p.charAt(0).toUpperCase() + p.slice(1)}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>

      <Divider />

      <Typography variant="overline" sx={{ px: 2, pt: 2, color: "text.secondary" }}>
        Status
      </Typography>
      <List dense>
        <ListItem disablePadding>
          <ListItemButton
            selected={isActive("/todos", { status: "pending" })}
            onClick={() => navigateWithFilter({ status: "pending" })}
          >
            <ListItemIcon>
              <HourglassEmptyIcon sx={{ color: statusColors.pending }} />
            </ListItemIcon>
            <ListItemText primary="Pending" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            selected={isActive("/todos", { status: "in_progress" })}
            onClick={() => navigateWithFilter({ status: "in_progress" })}
          >
            <ListItemIcon>
              <PlayCircleOutlineIcon sx={{ color: statusColors.in_progress }} />
            </ListItemIcon>
            <ListItemText primary="In Progress" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            selected={isActive("/todos", { status: "completed" })}
            onClick={() => navigateWithFilter({ status: "completed" })}
          >
            <ListItemIcon>
              <CheckCircleIcon sx={{ color: statusColors.completed }} />
            </ListItemIcon>
            <ListItemText primary="Completed" />
          </ListItemButton>
        </ListItem>
      </List>

      <Box sx={{ flexGrow: 1 }} />

      <Divider />
      <List dense>
        <ListItem disablePadding>
          <ListItemButton
            selected={pathname === "/profile"}
            onClick={() => {
              router.push("/profile");
              if (variant === "temporary") onClose();
            }}
          >
            <ListItemIcon>
              <PersonIcon />
            </ListItemIcon>
            <ListItemText primary="Profile" />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Drawer
      variant={variant}
      open={open}
      onClose={onClose}
      sx={{
        width: SIDEBAR_WIDTH,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: SIDEBAR_WIDTH,
          boxSizing: "border-box",
          ...(variant === "permanent" ? { mt: "64px" } : {}),
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
}
