import { getStatusColor } from '../utils/formatters'

// Stat card for dashboard metrics
const StatCard = ({
  title,
  value,
  unit = '',
  change,
  changeLabel,
  icon,
  color = 'green',
  className = '',
}) => {
  const colorMap = {
    green: 'from-[#2E7D32] to-[#388E3C]',
    orange: 'from-[#FF9800] to-[#F57C00]',
    blue: 'from-[#1565C0] to-[#1976D2]',
    teal: 'from-[#00695C] to-[#00897B]',
    red: 'from-[#C62828] to-[#E53935]',
    purple: 'from-[#6A1B9A] to-[#8E24AA]',
  }

  const isPositive = change > 0

  return (
    <div
      className={`
        relative overflow-hidden rounded-2xl p-6 text-white shadow-md
        bg-gradient-to-br ${colorMap[color] || colorMap.green}
        ${className}
      `}
    >
      {/* Background decoration */}
      <div className="absolute -top-4 -right-4 w-24 h-24 bg-white/10 rounded-full" />
      <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-white/5 rounded-full" />

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <p className="text-white/80 text-sm font-medium uppercase tracking-wide">{title}</p>
          {icon && (
            <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center text-xl">
              {icon}
            </div>
          )}
        </div>

        <p className="text-3xl font-extrabold tracking-tight">
          {value}
          {unit && <span className="text-lg font-medium ml-1 opacity-80">{unit}</span>}
        </p>

        {change !== undefined && (
          <p className="mt-2 text-sm font-medium">
            <span className={isPositive ? 'text-green-200' : 'text-red-200'}>
              {isPositive ? '▲' : '▼'} {Math.abs(change)}%
            </span>
            {changeLabel && <span className="text-white/70 ml-1">{changeLabel}</span>}
          </p>
        )}
      </div>
    </div>
  )
}

export default StatCard
