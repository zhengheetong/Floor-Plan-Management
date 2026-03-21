// src/components/InfoPanel.jsx
import StoreIcon from './StoreIcon';

export default function InfoPanel({ store }) {
  if (!store) {
    return (
      <div className="empty-state">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <p>Select a store on the map to view details.</p>
      </div>
    );
  }

  return (
    <div className="store-details">
      {/* 1. Added the StoreIcon component here */}
      <div style={{ marginBottom: '16px' }}>
        <StoreIcon 
          spriteX={store.spriteX} 
          spriteY={store.spriteY} 
          name={store.name} 
        />
      </div>

      <span className="store-category">{store.category}</span>
      <h2 className="store-name">{store.name}</h2>
      <p className="store-desc">{store.description}</p>
      
      <div className={`status-badge ${store.status.toLowerCase()}`}>
        <span className="status-dot">•</span>
        {store.status}
      </div>
    </div>
  );
}