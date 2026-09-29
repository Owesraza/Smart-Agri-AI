// Reusable Input component with label, icon, and error state
const Input = ({
  label,
  id,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  error,
  helperText,
  icon,
  iconPosition = 'left',
  required = false,
  disabled = false,
  className = '',
  inputClassName = '',
}) => {
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      {label && (
        <label
          htmlFor={id}
          className="text-sm font-semibold text-[#333333]"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        {icon && iconPosition === 'left' && (
          <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none">
            {icon}
          </span>
        )}

        <input
          id={id}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          placeholder={placeholder}
          required={required}
          disabled={disabled}
          className={`
            w-full rounded-xl border bg-white text-[#333333] text-base placeholder-gray-400
            transition-all duration-200
            ${icon && iconPosition === 'left' ? 'pl-10' : 'pl-4'}
            ${icon && iconPosition === 'right' ? 'pr-10' : 'pr-4'}
            py-3
            focus:outline-none focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent
            ${error ? 'border-red-500 bg-red-50' : 'border-gray-200 hover:border-gray-300'}
            ${disabled ? 'opacity-50 cursor-not-allowed bg-gray-50' : ''}
            ${inputClassName}
          `}
        />

        {icon && iconPosition === 'right' && (
          <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none">
            {icon}
          </span>
        )}
      </div>

      {error && (
        <p className="text-sm text-red-600 flex items-center gap-1">
          <span>⚠️</span> {error}
        </p>
      )}
      {!error && helperText && (
        <p className="text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  )
}

export default Input
