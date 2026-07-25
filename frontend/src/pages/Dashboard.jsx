import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import TransactionFeed from "../components/TransactionFeed";
import WalletGraph from "../components/WalletGraph";
import Pipeline from "../components/Pipeline";
import AlertPanel from "../components/AlertPanel";
import Timeline from "../components/Timeline";

import { Grid, Box } from "@mui/material";

function Dashboard() {
  return (
    <Box sx={{ display: "flex" }}>
      <Sidebar />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          ml: "240px",
          minHeight: "100vh",
          background: "#0B1020",
        }}
      >
        <Header />

        <Grid container spacing={2} sx={{ p: 2 }}>
          {/* Statistics Cards */}

          <Grid size={{ xs: 12, md: 3 }}>
            <StatCard title="Transactions" value="15,842" />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <StatCard title="Threats Detected" value="134" />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <StatCard title="Detection Time" value="198 ms" />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <StatCard title="Risk Level" value="LOW" />
          </Grid>

          {/* Second Row */}

          <Grid size={{ xs: 12, md: 6 }}>
            <TransactionFeed />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <WalletGraph />
          </Grid>

          {/* Third Row */}

          <Grid size={{ xs: 12, md: 6 }}>
            <Pipeline />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <AlertPanel />
          </Grid>

          {/* Bottom */}

          <Grid size={12}>
            <Timeline />
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}

export default Dashboard;