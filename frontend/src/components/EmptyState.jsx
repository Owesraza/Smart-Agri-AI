// Empty state placeholder component
const EmptyState = ({
  icon = '📭',
  title = 'Nothing here yet',
  description = 'No items to display at the moment.',
  action,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="text-6xl mb-4 opacity-80">{icon}</div>
      <h3 className="text-xl font-bold text-[#333333] mb-2">{title}</h3>
      <p className="text-gray-500 max-w-xs mb-6">{description}</p>
      {action && action}
    </div>
  )
}

export default EmptyState
