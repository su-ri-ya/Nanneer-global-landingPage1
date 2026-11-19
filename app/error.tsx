"use client"

import React, { useEffect } from "react"

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error("Application error boundary caught:", error)
  }, [error])

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <div className="bg-white p-6 rounded-xl border border-rose-200 shadow-md max-w-md w-full text-center">
        <h2 className="text-lg font-bold text-rose-700 mb-2">Something went wrong</h2>
        <p className="text-xs text-slate-600 mb-4">{error.message || "An unexpected error occurred."}</p>
        <button
          onClick={() => reset()}
          className="px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white rounded-lg text-xs font-semibold transition-colors"
        >
          Try Again
        </button>
      </div>
    </div>
  )
}
