import Pin from './Pin';

export default function Map({ activeFloor, stores, selectedStore, onStoreSelect }) {
  return (
    <svg viewBox="0 0 800 600" className="map-svg" style={{ width: '100%', height: '100%' }}>
      
      {/* This is where the magic happens! 
        Because it's in the public folder, this path works perfectly.
      */}
      <image 
        href={`/Floor/${activeFloor}/map.png`} 
        width="800" 
        height="600" 
        preserveAspectRatio="xMidYMid slice"
      />

      {stores.map((store) => (
        <Pin 
          key={store.id} 
          store={store} 
          isSelected={selectedStore?.id === store.id}
          onClick={() => onStoreSelect(store)} 
        />
      ))}
    </svg>
  );
}