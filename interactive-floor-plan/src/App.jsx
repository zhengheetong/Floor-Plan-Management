import { useState, useEffect } from "react";
import Map from "./components/Map";
import InfoPanel from "./components/InfoPanel";

export default function App() {
  const [activeFloor, setActiveFloor] = useState("0");
  const [selectedStore, setSelectedStore] = useState(null);

  const [floorConfig, setFloorConfig] = useState([]);
  const [currentFloorStores, setCurrentFloorStores] = useState([]); // Replaces the old static filter

  // 1. Fetch the master configuration on app load
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}Floor/floors.json`)
      .then((response) => response.json())
      .then((data) => setFloorConfig(data))
      .catch((error) => console.error("Error loading floor config:", error));
  }, []);

  // 2. Fetch the specific floor data whenever 'activeFloor' changes
  useEffect(() => {
    if (!activeFloor) return; // Guard clause

    fetch(`${import.meta.env.BASE_URL}Floor/${activeFloor}/data.json`)
      .then((response) => {
        if (!response.ok) throw new Error("Data not found");
        return response.json();
      })
      .then((data) => {
        setCurrentFloorStores(data);
        setSelectedStore(null); // Clear the sidebar when switching floors
      })
      .catch((error) => {
        console.error(`Error loading data for floor ${activeFloor}:`, error);
        setCurrentFloorStores([]); // Clear pins if no data exists
      });
  }, [activeFloor]); // This array tells React to run this effect ONLY when activeFloor changes

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">MegaMall Navigator</h1>

        <div className="floor-controls">
          {floorConfig.map((floor) => (
            <button
              key={floor.folder}
              className={`floor-btn ${activeFloor === floor.folder ? "active" : ""}`}
              onClick={() => setActiveFloor(floor.folder)}
            >
              {floor.name}
            </button>
          ))}
        </div>
      </header>

      <main className="main-layout">
        <div className="map-container">
          <Map
            activeFloor={activeFloor}
            stores={currentFloorStores}
            selectedStore={selectedStore}
            onStoreSelect={setSelectedStore}
          />
        </div>

        <div className="info-panel">
          <InfoPanel store={selectedStore} />
        </div>
      </main>
    </div>
  );
}
