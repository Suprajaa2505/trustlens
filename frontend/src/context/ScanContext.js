import { createContext, useContext, useState } from "react";

const ScanContext = createContext();

export function ScanProvider({ children }) {
  const [scanData, setScanData] = useState(null);
  const [trustData, setTrustData] = useState(null);
  const [scannedUrl, setScannedUrl] = useState("");

  return (
    <ScanContext.Provider value={{ scanData, setScanData, trustData, setTrustData, scannedUrl, setScannedUrl }}>
      {children}
    </ScanContext.Provider>
  );
}

export function useScan() {
  return useContext(ScanContext);
}