import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ScanProvider } from "./context/ScanContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Results from "./pages/Results";

function App() {
  return (
    <ScanProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </Router>
    </ScanProvider>
  );
}

export default App;