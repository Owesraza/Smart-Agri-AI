import { getStatusColor } from '../utils/formatters'
import { useLanguage } from '../context/LanguageContext'

// Task card for workflow and dashboard
const TaskCard = ({ task, onToggle }) => {
  const { t } = useLanguage()
  const isCompleted = task.status === 'Completed'

  const translatedPriority = t(`status.${task.priority?.toLowerCase()}`, task.priority)
  const translatedCrop = task.crop && task.crop !== '-' ? t(`crops.${task.crop?.toLowerCase()}`, task.crop) : null

  return (
    <div
      onClick={() => onToggle && onToggle(task.id)}
      className={`
        flex items-start gap-4 p-4 rounded-xl border transition-all duration-200 cursor-pointer select-none
        ${isCompleted ? 'bg-green-50 border-green-100 opacity-75' : 'bg-white border-gray-100 hover:border-[#2E7D32]/30 hover:shadow-sm'}
      `}
    >
      {/* Checkbox */}
      <button
        type="button"
        onClick={(e) => { e.stopPropagation(); onToggle && onToggle(task.id) }}
        className={`
          w-5 h-5 rounded-full border-2 flex-shrink-0 mt-0.5 cursor-pointer transition-all
          ${isCompleted ? 'bg-[#2E7D32] border-[#2E7D32]' : 'border-gray-300 hover:border-[#2E7D32]'}
        `}
        aria-label={isCompleted ? 'Mark as pending' : 'Mark as complete'}
      >
        {isCompleted && <span className="flex items-center justify-center w-full h-full text-white text-xs">✓</span>}
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-semibold ${isCompleted ? 'line-through text-gray-400' : 'text-[#333333]'}`}>
          {task.title}
        </p>
        <div className="flex flex-wrap items-center gap-2 mt-1.5">
          <span className="text-xs text-gray-400">📅 {task.dueDate}</span>
          {translatedCrop && (
            <span className="text-xs text-gray-400">🌾 {translatedCrop}</span>
          )}
        </div>
      </div>

      {/* Priority badge */}
      <span className={`text-xs font-semibold px-2.5 py-1 rounded-full flex-shrink-0 ${getStatusColor(task.priority)}`}>
        {translatedPriority}
      </span>
    </div>
  )
}

export default TaskCard
