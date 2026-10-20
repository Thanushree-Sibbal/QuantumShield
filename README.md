# Post-Quantum Blockchain Anomaly Detection System (its still ongoing)

An integrated project for screening wallet transfers, applying post-quantum signatures, recording approved transactions through Ethereum-compatible smart contracts, and reviewing alerts in a web dashboard.

## Project layout

```text
ai-oracle/          FastAPI transaction risk service and trained Random Forest
backend/            Express API, authentication, MongoDB, orchestration, Ethers.js
blockchain/         Solidity contracts and Hardhat deployment
dataset_generator/  Synthetic transaction data and training utilities
docs/               Architecture alignment and run guide
frontend/           React + Vite user and admin application
pq-service/         FastAPI ML-DSA signing and verification service (liboqs)
```

The AI Oracle combines its trained 44-feature Random Forest with QuantumShield historical wallet intelligence. QuantumShield's raw graph/sequence data, precomputed 32-dimensional GraphSAGE and 32-dimensional LSTM embeddings, and source model weights are included under `ai-oracle/datasets/chain_intelligence/`. The 64-dimensional fusion embeddings are used to train the Isolation Forest stage. At transaction time, known sender/receiver addresses are looked up and rescored with that model; matched reputation raises the existing wallet-risk feature before the transaction Random Forest evaluates the transfer. This signal is advisory and does not override an invalid PQ signature or on-chain blocked-wallet result.

The administrator console's **Chain Intelligence** page reports the model pipeline, source graph/sequence coverage, and highest scoring historical wallets. The connected page is available at `/admin/model`. A read-only snapshot view at `/demo/chain-intelligence` can be used to preview the UI without an admin login. This demo snapshot is for presentation and does not execute a fresh model request. Start the frontend and open `/demo/recording.html` to generate an animated model walkthrough; the generated video is also included at `docs/demo/chain-intelligence-walkthrough.webm`.

## Local setup

Prerequisites: Node.js 20+, Python 3.12+, MongoDB, and a local EVM JSON-RPC node such as Hardhat. The PQ service also needs liboqs available for its `liboqs-python` dependency. Each component runs in its own terminal.

1. Start MongoDB. From `blockchain/`, run `npm ci`, then start the local EVM node with `npm run node` in a terminal.
2. Deploy contracts to that node. In another terminal, from `blockchain/`, run `npx hardhat run scripts/deploy.ts --network localhost`. Copy the four printed addresses into `backend/.env`.
3. Start the AI Oracle. To recreate the chain fusion model/scores from the included fused dataset, first run `python -m app.training.train_chain_model` once. The generated artifacts are included in this folder, so ordinary startup does not require retraining.

   ```powershell
   cd ai-oracle
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

4. Start the PQ service in a separate terminal using the same virtual-environment steps from `pq-service/`, install its `requirements.txt`, then run `uvicorn app.main:app --host 127.0.0.1 --port 8001`.
5. Copy `backend/.env.example` to `backend/.env`. Set MongoDB, JWT, local RPC and deployed contract addresses, AI/PQ URLs, and a development-only encryption secret/private key. The included development key is a public Hardhat test key. Do not reuse sample secrets outside a local demo.
6. From `backend/`, run `npm ci` and `npm run dev`.
7. From `frontend/`, run `npm ci` and `npm run dev`. The frontend defaults to `http://localhost:5000/api/v1`, which matches the backend. Open the URL printed by Vite.

Register a user, register a wallet, then initiate a transfer. The application routes it through the PQ signing/verification service, risk oracle, administrator review when required, and the EVM ledger when approved. Contract calls and wallet setup require the local node, deployed addresses, and funded development accounts to match the backend configuration.

## Components and API entry points

- Frontend: React/Vite app in `frontend/`.
- Backend: REST API at `/api`; root `GET /` is a health check.
- AI Oracle: `GET /`, `POST /prediction/`, and `GET /chain-risk/overview` on port 8000.
- PQ service: `GET /` plus key-generation, signing, and verification routes on port 8001.
- Contracts: WalletRegistry, TransactionLedger, SecurityManager, and OracleController in `blockchain/contracts/`.

Component-specific details and environment templates live beside each service. The reviewed architecture comparison is in [`docs/ARCHITECTURE_ALIGNMENT.md`](docs/ARCHITECTURE_ALIGNMENT.md).

## Important scope notes

- This is a local academic prototype, not a production Ethereum validator or mempool firewall. Its screening happens in the application transaction path before the application submits an approved transfer.
- GraphSAGE and LSTM embeddings are precomputed over the included historical dataset. This project does not run GNN/LSTM inference on a live mempool or create embeddings for unseen wallets at request time. Unmatched addresses are unscored by the chain-intelligence stage.
- The 0–1 “anomaly probability” is a bounded transformation of Isolation Forest decision scores, not a calibrated probability. Treat scores as ranking signals for the academic demo.
- The request report uses “Kyber” for encapsulation, while this code's PQ service implements ML-DSA signatures (Dilithium's standardized name). It does not implement ML-KEM/Kyber key encapsulation.
- Do not treat the sample model or synthetic training data as a validated fraud detector. Reproduce and evaluate models on a documented labeled dataset before making operational decisions.

## License

MIT for the original application code where specified. Third-party dependencies and included research artifacts retain their respective licenses and attribution.
