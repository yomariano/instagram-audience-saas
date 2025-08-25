'use client'

import { useState } from 'react'
import { Analytics, Camera, TrendingUp, Users } from 'lucide-react'
import DashboardCard from './components/DashboardCard'
import AddAccountForm from './components/AddAccountForm'
import DemographicsChart from './components/DemographicsChart'

export default function Home() {
  const [activeAccount, setActiveAccount] = useState<string | null>(null)

  return (
    <main className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="flex items-center justify-center gap-3 mb-4">
          <Camera className="h-8 w-8 text-purple-600" />
          <h1 className="text-4xl font-bold text-gray-900">
            Instagram Audience Analysis
          </h1>
        </div>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover your audience demographics with AI-powered analysis of Instagram comments and engagement patterns
        </p>
      </div>

      {/* Add Account Form */}
      <div className="mb-12">
        <AddAccountForm onAccountAdded={setActiveAccount} />
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <DashboardCard
          icon={<Users className="h-6 w-6" />}
          title="Total Commenters"
          value="1,247"
          change="+12%"
          changeType="increase"
        />
        <DashboardCard
          icon={<TrendingUp className="h-6 w-6" />}
          title="Engagement Rate"
          value="5.2%"
          change="+0.8%"
          changeType="increase"
        />
        <DashboardCard
          icon={<Analytics className="h-6 w-6" />}
          title="Analysis Complete"
          value="89%"
          change="Processing..."
          changeType="neutral"
        />
      </div>

      {/* Demographics */}
      {activeAccount && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Audience Demographics</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <DemographicsChart 
              title="Gender Distribution"
              data={[
                { name: 'Female', value: 55, fill: '#8B5CF6' },
                { name: 'Male', value: 45, fill: '#06B6D4' }
              ]}
            />
            <DemographicsChart 
              title="Age Distribution" 
              data={[
                { name: '18-24', value: 30, fill: '#10B981' },
                { name: '25-34', value: 40, fill: '#F59E0B' },
                { name: '35-44', value: 20, fill: '#EF4444' },
                { name: '45+', value: 10, fill: '#6B7280' }
              ]}
            />
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="text-center py-8 border-t border-gray-200">
        <p className="text-gray-500">
          Powered by AI • Built with Next.js and FastAPI
        </p>
      </footer>
    </main>
  )
}