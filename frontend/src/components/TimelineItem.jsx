import { getStatusColor } from '../utils/formatters'

// Timeline item for Workflow page
const TimelineItem = ({ step, isLast = false }) => {
  const statusIcons = {
    Completed: '✅',
    'In Progress': '🔄',
    Upcoming: '⏳',
  }

  const lineColors = {
    Completed: 'bg-[#2E7D32]',
    'In Progress': 'bg-[#FF9800]',
    Upcoming: 'bg-gray-200',
  }

  const dotColors = {
    Completed: 'bg-[#2E7D32] border-[#2E7D32]',
    'In Progress': 'bg-[#FF9800] border-[#FF9800]',
    Upcoming: 'bg-white border-gray-300',
  }

  return (
    <div className="flex gap-5">
      {/* Timeline dot + line */}
      <div className="flex flex-col items-center flex-shrink-0">
        <div
          className={`w-4 h-4 rounded-full border-2 ${dotColors[step.status]} flex-shrink-0 mt-1 z-10`}
        />
        {!isLast && (
          <div className={`w-0.5 flex-1 mt-1 ${lineColors[step.status]} opacity-30 min-h-8`} />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 pb-8">
        <div className="flex items-start justify-between flex-wrap gap-2">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-base">{statusIcons[step.status]}</span>
              <h3 className="text-base font-bold text-[#333333]">{step.title}</h3>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${getStatusColor(step.status)}`}>
                {step.status}
              </span>
            </div>
            <p className="text-sm text-gray-500 mt-0.5">📅 {step.date}</p>
          </div>
        </div>

        <p className="text-sm text-gray-600 mt-2 mb-3">{step.description}</p>

        {/* Sub-tasks */}
        {step.tasks && (
          <div className="space-y-1.5">
            {step.tasks.map((task, idx) => (
              <div key={idx} className="flex items-center gap-2 text-sm text-gray-600">
                <span className={`w-4 h-4 rounded-full flex-shrink-0 flex items-center justify-center text-xs
                  ${step.status === 'Completed' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}
                `}>
                  {step.status === 'Completed' ? '✓' : '○'}
                </span>
                {task}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default TimelineItem
