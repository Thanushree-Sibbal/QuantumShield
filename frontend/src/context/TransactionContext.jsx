import React, { createContext, useContext, useEffect, useState } from "react";
import { connectWebSocket } from "../services/websocket";

const TransactionContext = createContext();

export const TransactionProvider = ({ children }) => {
  const [transactions, setTransactions] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const [stats, setStats] = useState({
    totalTransactions: 0,
    highRisk: 0,
    mediumRisk: 0,
    lowRisk: 0,
    highestRiskScore: 0,
  });

  const [graphData, setGraphData] = useState({
    nodes: [],
    edges: [],
  });

  useEffect(() => {
    connectWebSocket((tx) => {
      console.log("Incoming Transaction:", tx);

      const transaction = {
        ...tx,
        id: `${tx.tx_hash || Date.now()}-${Math.random()}`,
      };

      // -------------------------
      // Transaction Feed
      // -------------------------
      setTransactions((prev) => [
        transaction,
        ...prev.slice(0, 49),
      ]);

      // -------------------------
      // Alerts
      // -------------------------
      if (tx.status === "High" || tx.status === "Medium") {
        setAlerts((prev) => [
          {
            id: transaction.id,
            wallet: tx.from_address,
            risk: tx.status,
            score: tx.risk_score,
            timestamp: tx.timestamp,
          },
          ...prev.slice(0, 19),
        ]);
      }

      // -------------------------
      // Dashboard Statistics
      // -------------------------
      setStats((prev) => ({
        totalTransactions: prev.totalTransactions + 1,
        highRisk: prev.highRisk + (tx.status === "High" ? 1 : 0),
        mediumRisk: prev.mediumRisk + (tx.status === "Medium" ? 1 : 0),
        lowRisk: prev.lowRisk + (tx.status === "Low" ? 1 : 0),
        highestRiskScore: Math.max(
          prev.highestRiskScore,
          tx.risk_score || 0
        ),
      }));

      // -------------------------
      // Wallet Graph
      // -------------------------
      setGraphData((prev) => {
        const nodes = [...prev.nodes];
        const edges = [...prev.edges];

        const nodeExists = (id) =>
          nodes.find((node) => node.id === id);

        const edgeExists = (source, target) =>
          edges.find(
            (edge) =>
              edge.source === source &&
              edge.target === target
          );

        const randomPosition = () => ({
          x: 100 + Math.random() * 800,
          y: 50 + Math.random() * 500,
        });

        // Sender
        if (!nodeExists(tx.from_address)) {
          nodes.push({
            id: tx.from_address,
            data: {
              label:
                tx.from_address.substring(0, 6) +
                "..." +
                tx.from_address.slice(-4),
            },
            position: randomPosition(),
            style: {
             background:
             tx.status === "High"
             ? "#ef4444"
             : tx.status === "Medium"
             ? "#f59e0b"
             : "#22c55e",

            color: "#fff",
             border: "2px solid rgba(255,255,255,0.9)",
            borderRadius: "50%",

            width: 58,
            height: 58,

            fontSize: 10,
            fontWeight: "bold",

            boxShadow:
            tx.status === "High"
            ? "0 0 18px rgba(239,68,68,0.85)"
            : tx.status === "Medium"
            ? "0 0 18px rgba(245,158,11,0.8)"
            : "0 0 18px rgba(34,197,94,0.8)",

            transition: "all .3s ease",
            },
          });
        }

        // Receiver
        if (!nodeExists(tx.to_address)) {
          nodes.push({
            id: tx.to_address,
            data: {
              label:
                tx.to_address.substring(0, 6) +
                "..." +
                tx.to_address.slice(-4),
            },
            position: randomPosition(),
            style: {
            background: "#3b82f6",

            color: "#fff",

            borderRadius: "50%",

            border: "2px solid rgba(255,255,255,0.9)",

            width: 58,
            height: 58,

            fontSize: 10,
            fontWeight: "bold",

            boxShadow: "0 0 16px rgba(59,130,246,.8)",

            transition: "all .3s ease",
            },
          });
        }

        // Edge
        if (!edgeExists(tx.from_address, tx.to_address)) {
          edges.push({
            id: transaction.id,
            source: tx.from_address,
            target: tx.to_address,
            animated: true,
            type: "smoothstep",
            style: {
            stroke:
            tx.status === "High"
            ? "#ef4444"
            : tx.status === "Medium"
            ? "#f59e0b"
             : "#22c55e",

            strokeWidth: 2.8,

            opacity: 0.9,
            },
          });
        }

        return {
          nodes: nodes.slice(-60),
          edges: edges.slice(-80),
        };
      });
    });
  }, []);

  return (
    <TransactionContext.Provider
      value={{
        transactions,
        alerts,
        stats,
        graphData,
      }}
    >
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = () => useContext(TransactionContext);