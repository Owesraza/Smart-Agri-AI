// Search bar component
const SearchBar = ({
  value,
  onChange,
  placeholder = 'Search...',
  className = '',
}) => {
  return (
    <div className={`relative ${className}`}>
      <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none">
        🔍
      </span>
      <input
        type="search"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="
          w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200
          bg-white text-[#333333] text-base placeholder-gray-400
          focus:outline-none focus:ring-2 focus:ring-[#2E7D32] focus:border-transparent
          hover:border-gray-300 transition-all duration-200
        "
      />
    </div>
  )
}

export default SearchBar
