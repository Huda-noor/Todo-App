export default function EmptyState() {
  return (
    <div className="empty-state" role="status">
      <div className="empty-state-icon" aria-hidden="true">
        📝
      </div>
      <h2 className="empty-state-title">No todos yet</h2>
      <p>Create your first todo!</p>
    </div>
  );
}
