// src/components/Pin.jsx
export default function Pin({ store, isSelected, onClick }) {
  return (
    <g
      transform={`translate(${store.x}, ${store.y})`}
      onClick={onClick}
      style={{ cursor: "pointer" }}
    >
      {/* Pin Shadow */}
      <ellipse cx="0" cy="15" rx="12" ry="6" fill="rgba(0,0,0,0.15)" />

      {/* Pin Body */}
      <path
        d="M 0 15 C -15 0 -15 -20 0 -20 C 15 -20 15 0 0 15 Z"
        fill={isSelected ? "#ef4444" : "#3b82f6"}
        stroke="#ffffff"
        strokeWidth="2"
        style={{ transition: "fill 0.2s ease-in-out" }}
      />

      {/* Pin Inner Dot */}
      <circle cx="0" cy="-6" r="4" fill="#ffffff" />

      {/* Floating Store Label */}
      <text
        x="0"
        y="-28"
        textAnchor="middle"
        fill="#1e293b"
        fontSize="14"
        fontWeight="bold"
        style={{ pointerEvents: "none" }}
      >
        {store.name}
      </text>
    </g>
  );
}
