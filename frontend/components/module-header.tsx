export function ModuleHeader({ title, description }: { title: string; description: string }) {
  return (
    <div className="module-header">
      <div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
    </div>
  );
}
