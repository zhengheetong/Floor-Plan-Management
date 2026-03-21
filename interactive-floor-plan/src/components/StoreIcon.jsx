// src/components/StoreIcon.jsx
export default function StoreIcon({ spriteX, spriteY, name }) {
  const iconSize = 64; // The standard size we will use for all logos

  return (
    <div 
      title={name}
      style={{
        width: `${iconSize}px`,
        height: `${iconSize}px`,
        // We will put the actual sprite sheet in the public folder later
        backgroundImage: `url('/icons-sprite.png')`, 
        backgroundRepeat: 'no-repeat',
        // Shift the image negatively to frame the correct icon
        backgroundPosition: `-${spriteX}px -${spriteY}px`,
        backgroundColor: '#f1f5f9', // Placeholder background color
        borderRadius: '12px',
        border: '1px solid #e2e8f0',
        boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'
      }} 
    />
  );
}