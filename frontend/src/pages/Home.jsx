import { useState } from "react";
import Header from "../components/Header";
import api from "../services/api";

function Home() {

    const [wallet, setWallet] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const analyzeWallet = async () => {

        if (!wallet.trim()) {
            setError("Please enter a wallet address.");
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {

            const response = await api.post("/predict", {
                wallet: wallet
            });

            setResult(response.data);

        } catch (err) {

            if (err.response) {
                setError(err.response.data.detail);
            } else {
                setError("Unable to connect to backend.");
            }

        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Header />

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "80vh"
                }}
            >
                <div
                    style={{
                        background: "#1F2937",
                        padding: "40px",
                        borderRadius: "15px",
                        width: "550px",
                        boxShadow: "0 0 25px rgba(0,229,255,0.2)"
                    }}
                >
                    <h2>Analyze Ethereum Wallet</h2>

                    <p
                        style={{
                            color: "#9CA3AF",
                            marginTop: "10px",
                            marginBottom: "25px"
                        }}
                    >
                        Enter a wallet address to detect suspicious blockchain activity.
                    </p>

                    <input
                        type="text"
                        value={wallet}
                        onChange={(e) => setWallet(e.target.value)}
                        placeholder="Enter wallet address..."
                        style={{
                            width: "100%",
                            padding: "14px",
                            borderRadius: "8px",
                            border: "none",
                            fontSize: "16px",
                            marginBottom: "20px"
                        }}
                    />

                    <button
                        onClick={analyzeWallet}
                        style={{
                            width: "100%",
                            padding: "14px",
                            background: "#00E5FF",
                            border: "none",
                            borderRadius: "8px",
                            cursor: "pointer",
                            fontWeight: "bold",
                            fontSize: "16px"
                        }}
                    >
                        Analyze Wallet
                    </button>

                    {loading && (
                        <p style={{ marginTop: "20px" }}>
                            Analyzing wallet...
                        </p>
                    )}

                    {error && (
                        <p
                            style={{
                                color: "red",
                                marginTop: "20px"
                            }}
                        >
                            {error}
                        </p>
                    )}

                    {result && (
                        <div
                            style={{
                                marginTop: "30px",
                                background: "#111827",
                                padding: "20px",
                                borderRadius: "10px"
                            }}
                        >
                            <h3>Prediction Result</h3>

                            <p><b>Wallet:</b> {result.wallet}</p>

                            <p><b>Prediction:</b> {result.prediction}</p>

                            <p><b>Risk Level:</b> {result.risk_level}</p>

                            <p><b>Risk Score:</b> {result.risk_score}</p>

                            <p><b>Anomaly Score:</b> {result.anomaly_score}</p>

                            <p><b>Model:</b> {result.model}</p>

                            <p><b>Analysis Time:</b> {result.analysis_time_ms} ms</p>
                        </div>
                    )}

                </div>
            </div>
        </>
    );
}

export default Home;