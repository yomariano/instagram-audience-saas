interface DashboardCardProps {
  icon: React.ReactNode
  title: string
  value: string
  change: string
  changeType: 'increase' | 'decrease' | 'neutral'
}

export default function DashboardCard({ icon, title, value, change, changeType }: DashboardCardProps) {
  const changeColor = {
    increase: 'text-green-600',
    decrease: 'text-red-600',
    neutral: 'text-gray-600'
  }[changeType]

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
      <div className="flex items-center justify-between mb-4">
        <div className="text-purple-600">
          {icon}
        </div>
        <span className={`text-sm font-medium ${changeColor}`}>
          {change}
        </span>
      </div>
      <div>
        <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  )
}