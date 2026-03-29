export default function StoreIcon({ spriteX, spriteY, name }) {
  // 1. Update the base size to match your new Python output exactly
  const baseSize = 120;

  // 2. We can drop the scale back down to 1 (or 0.8 if 120px feels TOO huge in the sidebar)
  const scale = 1;
  const finalSize = baseSize * scale;

  const hasSprite = spriteX !== undefined && spriteY !== undefined;

  return (
    <div style={{ width: `${finalSize}px`, height: `${finalSize}px` }}>
      <div
        title={name}
        style={{
          width: `${baseSize}px`,
          height: `${baseSize}px`,
          backgroundImage: hasSprite
            ? `url('${import.meta.env.BASE_URL}icons-sprite.png')`
            : "none",
          backgroundPosition: `-${spriteX}px -${spriteY}px`,
          backgroundRepeat: "no-repeat",
          backgroundColor: "#f8fafc",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "36px", // Bumped up the fallback font size too
          fontWeight: "bold",
          color: "#94a3b8",
          boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
          transform: `scale(${scale})`,
          transformOrigin: "top left",
        }}
      >
        {!hasSprite && name ? name.charAt(0).toUpperCase() : ""}
      </div>
    </div>
  );
}
