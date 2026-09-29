// Reusable Button component with multiple variants
const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  iconPosition = 'left',
  fullWidth = false,
  loading = false,
  disabled = false,
  onClick,
  type = 'button',
  className = '',
}) => {
  const base =
    'inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 active:scale-[0.98] cursor-pointer'

  const variants = {
    primary:
      'bg-[#2E7D32] hover:bg-[#1B5E20] text-white shadow-md hover:shadow-lg focus-visible:ring-[#2E7D32]',
    secondary:
      'bg-[#81C784] hover:bg-[#66BB6A] text-[#1B5E20] shadow-sm hover:shadow-md focus-visible:ring-[#81C784]',
    accent:
      'bg-[#FF9800] hover:bg-[#F57C00] text-white shadow-md hover:shadow-lg focus-visible:ring-[#FF9800]',
    outline:
      'border-2 border-[#2E7D32] text-[#2E7D32] hover:bg-[#2E7D32] hover:text-white focus-visible:ring-[#2E7D32]',
    ghost:
      'text-[#2E7D32] hover:bg-green-50 focus-visible:ring-[#2E7D32]',
    danger:
      'bg-red-600 hover:bg-red-700 text-white shadow-md hover:shadow-lg focus-visible:ring-red-500',
    white:
      'bg-white text-[#2E7D32] hover:bg-gray-50 shadow-md hover:shadow-lg focus-visible:ring-[#2E7D32]',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-base',
    lg: 'px-7 py-3.5 text-lg',
    xl: 'px-9 py-4 text-xl',
  }

  const disabledStyles = 'opacity-50 cursor-not-allowed pointer-events-none'

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        ${base}
        ${variants[variant]}
        ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        ${disabled || loading ? disabledStyles : ''}
        ${className}
      `}
    >
      {loading ? (
        <span className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
      ) : (
        <>
          {icon && iconPosition === 'left' && <span className="text-[1.1em]">{icon}</span>}
          {children}
          {icon && iconPosition === 'right' && <span className="text-[1.1em]">{icon}</span>}
        </>
      )}
    </button>
  )
}

export default Button
