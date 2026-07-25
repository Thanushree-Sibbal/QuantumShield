import { useEffect, useState } from "react";
import { connectWebSocket } from "../services/websocket";

import {
  Card,
  CardContent,
  Typography,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Box,
} from "@mui/material";

export default function TransactionFeed() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    connectWebSocket((tx) => {
      const date = new Date(tx.timestamp * 1000);

      const formatted = {
        time: date.toLocaleTimeString(),

        from:
          tx.from_address.slice(0, 6) +
          "..." +
          tx.from_address.slice(-4),

        to:
          tx.to_address.slice(0, 6) +
          "..." +
          tx.to_address.slice(-4),

        amount:
          Number(tx.value_eth).toFixed(6) + " ETH",

        status: tx.status,
        riskScore: tx.risk_score,
      };

      setTransactions((prev) => [
        formatted,
        ...prev.slice(0, 24),
      ]);
    });

    return () => {};
  }, []);

  const getColor = (status) => {
    switch (status) {
      case "Low":
        return "success";

      case "Medium":
        return "warning";

      case "High":
        return "error";

      default:
        return "default";
    }
  };

  return (
    <Card
      sx={{
        background: "#151C32",
        border: "1px solid #27314E",
        borderRadius: 3,
        height: 500,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <CardContent
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
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
          📡 Live Ethereum Transaction Feed
        </Typography>

        <Box
          sx={{
            flex: 1,
            overflowY: "auto",

            "&::-webkit-scrollbar": {
              width: "8px",
            },

            "&::-webkit-scrollbar-thumb": {
              background: "#27314E",
              borderRadius: "10px",
            },
          }}
        >
          <Table
            stickyHeader
            sx={{
              tableLayout: "fixed",
              width: "100%",
            }}
          >
            <TableHead>
              <TableRow>
                <TableCell
                  sx={{
                    background: "#151C32",
                    color: "#00E5FF",
                    fontWeight: "bold",
                    width: "18%",
                  }}
                >
                  Time
                </TableCell>

                <TableCell
                  sx={{
                    background: "#151C32",
                    color: "#00E5FF",
                    fontWeight: "bold",
                    width: "21%",
                  }}
                >
                  From
                </TableCell>

                <TableCell
                  sx={{
                    background: "#151C32",
                    color: "#00E5FF",
                    fontWeight: "bold",
                    width: "21%",
                  }}
                >
                  To
                </TableCell>

                <TableCell
                  sx={{
                    background: "#151C32",
                    color: "#00E5FF",
                    fontWeight: "bold",
                    width: "18%",
                  }}
                >
                  Amount
                </TableCell>

                <TableCell
                  align="center"
                  sx={{
                    background: "#151C32",
                    color: "#00E5FF",
                    fontWeight: "bold",
                    width: "22%",
                  }}
                >
                  AI Risk Assessment
                </TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {transactions.map((tx, index) => (
                <TableRow
                  key={index}
                  hover
                  sx={{
                    "&:hover": {
                      background: "#1D2845",
                    },
                  }}
                >
                  <TableCell sx={{ color: "#F3F4F6" }}>
                    {tx.time}
                  </TableCell>

                  <TableCell
                    sx={{
                      color: "#D1D5DB",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {tx.from}
                  </TableCell>

                  <TableCell
                    sx={{
                      color: "#D1D5DB",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {tx.to}
                  </TableCell>

                  <TableCell
                    sx={{
                      color: "#00E5FF",
                      fontWeight: "bold",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {tx.amount}
                  </TableCell>

                  <TableCell align="center">
                    <Chip
                      label={`${tx.status} (${tx.riskScore})`}
                      color={getColor(tx.status)}
                      size="small"
                      sx={{
                        minWidth: 120,
                        fontWeight: "bold",
                        fontSize: "0.8rem",
                      }}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </CardContent>
    </Card>
  );
}