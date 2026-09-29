// Reusable Card component
const Card = ({
  children,
  className = '',
  padding = true,
  hoverable = false,
  onClick,
  border = false,
  id,
}) => {
  return (
    <div
      id={id}
      onClick={onClick}
      className={`
        bg-[#F8F9FA] rounded-2xl shadow-sm
        ${padding ? 'p-5 sm:p-6' : ''}
        ${border ? 'border border-gray-100' : ''}
        ${hoverable ? 'hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 cursor-pointer' : ''}
        ${onClick ? 'cursor-pointer' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  )
}

export const CardHeader = ({ title, subtitle, action, icon }) => (
  <div className="flex items-start justify-between mb-4">
    <div className="flex items-center gap-3">
      {icon && (
        <div className="w-10 h-10 rounded-xl bg-[#2E7D32]/10 flex items-center justify-center text-xl">
          {icon}
        </div>
      )}
      <div>
        <h3 className="text-base font-bold text-[#333333]">{title}</h3>
        {subtitle && <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>}
      </div>
    </div>
    {action && <div>{action}</div>}
  </div>
)

export default Card
