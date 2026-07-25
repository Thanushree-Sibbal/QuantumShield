import { Card, CardContent, Typography, Box } from "@mui/material";
import {
  ReactFlow,
  Background,
  Controls,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { useTransactions } from "../context/TransactionContext";

export default function WalletGraph() {
  const { graphData } = useTransactions();

  return (
    <Card
      sx={{
        background: "#151C32",
        border: "1px solid #27314E",
        borderRadius: 3,
        height: 500,
      }}
    >
      <CardContent
        sx={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Typography
          variant="h6"
          sx={{
            color: "white",
            fontWeight: "bold",
            mb: 2,
          }}
        >
          🌐 Live Wallet Network
        </Typography>

        <Box
          sx={{
            flex: 1,
            borderRadius: 2,
            overflow: "hidden",
            background: "#0B1020",
          }}
        >
          <ReactFlow
            nodes={graphData?.nodes || []}
            edges={graphData?.edges || []}
            fitView
            fitViewOptions={{
              padding: 0.25,
            }}
            proOptions={{
              hideAttribution: true,
            }}
          >
            <Background
            gap={28}
            size={1.2}
            color="#1F2A44"
              />

            <Controls />
          </ReactFlow>
        </Box>

        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            gap: 4,
            mt: 2,
            color: "#CBD5E1",
            fontSize: 13,
          }}
        >
          <span>🔴 High Risk</span>
          <span>🟠 Medium Risk</span>
          <span>🟢 Low Risk</span>
          <span>🔵 Receiver</span>
        </Box>
      </CardContent>
    </Card>
  );
}