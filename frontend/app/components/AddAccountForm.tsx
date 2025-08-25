'use client'

import { useState } from 'react'
import { Plus, Instagram, Loader2 } from 'lucide-react'

interface AddAccountFormProps {
  onAccountAdded: (username: string) => void
}

export default function AddAccountForm({ onAccountAdded }: AddAccountFormProps) {
  const [username, setUsername] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!username.trim()) return

    setIsLoading(true)
    setMessage('')

    try {
      const response = await fetch('/api/v1/accounts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username.replace('@', '') }),
      })

      const data = await response.json()

      if (response.ok) {
        setMessage(`✅ Analysis started for @${username}`)
        onAccountAdded(username)
        setUsername('')
      } else {
        setMessage(`❌ Error: ${data.detail || 'Failed to add account'}`)
      }
    } catch (error) {
      setMessage('❌ Network error. Please check if the API is running.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
      <div className="flex items-center gap-3 mb-6">
        <Instagram className="h-6 w-6 text-purple-600" />
        <h2 className="text-xl font-semibold text-gray-900">Add Instagram Account</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
            Instagram Username
          </label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">@</span>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
              className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={isLoading}
            />
          </div>
        </div>
        
        <button
          type="submit"
          disabled={isLoading || !username.trim()}
          className="w-full flex items-center justify-center gap-2 bg-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Plus className="h-5 w-5" />
          )}
          {isLoading ? 'Starting Analysis...' : 'Start Analysis'}
        </button>
      </form>

      {message && (
        <div className="mt-4 p-3 rounded-lg bg-gray-50 border border-gray-200">
          <p className="text-sm text-gray-700">{message}</p>
        </div>
      )}
    </div>
  )
}