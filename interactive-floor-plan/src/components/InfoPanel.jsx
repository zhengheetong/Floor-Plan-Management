import StoreIcon from "./StoreIcon";

export default function InfoPanel({ store, onClose }) {
  if (!store) {
    return (
      <div className="empty-state">
        <svg
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          style={{ width: 48, opacity: 0.3, marginBottom: 15 }}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p>Select a store on the map to view details.</p>
      </div>
    );
  }

  return (
    <div className="store-details">
      <button
        onClick={onClose}
        style={{
          float: "right",
          border: "none",
          background: "none",
          cursor: "pointer",
          fontSize: "24px",
          color: "#94a3b8",
        }}
      >
        ×
      </button>

      {/* Increased margin to accommodate the bigger logo */}
      <div style={{ marginBottom: "32px" }}>
        <StoreIcon
          spriteX={store.spriteX}
          spriteY={store.spriteY}
          name={store.name}
        />
      </div>

      <span className="store-category">{store.category}</span>
      <h2 className="store-name">{store.name}</h2>

      <div className="store-lot">Unit: {store.lot}</div>

      <p className="store-desc">{store.description}</p>
    </div>
  );
}
