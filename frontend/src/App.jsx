import Dashboard from "./pages/Dashboard";
import { TransactionProvider } from "./context/TransactionContext";

function App() {
  return (
    <TransactionProvider>
      <Dashboard />
    </TransactionProvider>
  );
}

export default App;