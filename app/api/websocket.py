import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.replay_service import replay
from app.api.predictor import predictor

router = APIRouter()


@router.websocket("/ws/transactions")
async def transaction_stream(websocket: WebSocket):

    await websocket.accept()

    print("✅ WebSocket Connected")

    try:
        while True:

            # Get next transaction
            tx = replay.next_transaction()

            # Predict sender wallet
            prediction = predictor.predict_wallet(tx["from_address"])

            status = "Unknown"
            risk_score = 0
            anomaly_score = 0

            if prediction["success"]:
                status = prediction["risk_level"]
                risk_score = prediction["risk_score"]
                anomaly_score = prediction["anomaly_score"]

            # Debug
            print("Sending transaction...")
            print({
                "tx_hash": tx["tx_hash"],
                "from": tx["from_address"],
                "to": tx["to_address"],
                "status": status,
                "risk_score": risk_score,
            })

            await websocket.send_json({
                "tx_hash": tx["tx_hash"],
                "block_number": int(tx["block_number"]),
                "timestamp": int(tx["timestamp"]),
                "from_address": tx["from_address"],
                "to_address": tx["to_address"],
                "value_eth": float(tx["value_eth"]),
                "gas": int(tx["gas"]),
                "gas_price": int(tx["gas_price"]),
                "nonce": int(tx["nonce"]),

                "status": status,
                "risk_score": risk_score,
                "anomaly_score": anomaly_score
            })

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("❌ WebSocket Disconnected")

    except Exception as e:
        print("❌ WebSocket Error:", e)