import React from "react"
import Link from "next/link"
import Image from "next/image"
import { Home, Activity, ArrowLeft } from "lucide-react"

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white via-sky-50/40 to-white flex flex-col items-center justify-center p-4 sm:p-8 font-sans selection:bg-sky-200 selection:text-sky-950">
      <div className="max-w-lg w-full text-center space-y-6">
        {/* Brand Logo */}
        <div className="flex justify-center">
          <Link href="/" className="inline-block" aria-label="Nanneer Consultancy Home">
            <div className="relative h-12 w-44">
              <Image
                src="/logo.png"
                alt="Nanneer Consultancy Logo"
                fill
                priority
                className="object-contain"
              />
            </div>
          </Link>
        </div>

        {/* 404 Badge & Heading */}
        <div className="space-y-2">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono font-bold bg-sky-100 text-sky-800 border border-sky-200">
            ERROR 404 · PAGE NOT FOUND
          </span>
          <h1 className="text-3xl sm:text-4xl font-black text-[#0B2545] tracking-tight">
            Pipeline Route Unavailable
          </h1>
          <p className="text-sm text-slate-600 max-w-md mx-auto leading-relaxed">
            The page you are looking for has been moved, renamed, or does not exist. Use the navigation links below to return to the active plant operations.
          </p>
        </div>

        {/* Helpful Direct Links to Preserve Crawl Equity */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-left">
          <Link
            href="/"
            className="p-3.5 rounded-xl bg-white border border-sky-100 hover:border-sky-300 shadow-xs hover:shadow-md transition-all group flex flex-col justify-between"
          >
            <div className="w-8 h-8 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center mb-2 group-hover:bg-sky-600 group-hover:text-white transition-colors">
              <Home className="w-4 h-4" />
            </div>
            <div>
              <span className="font-bold text-xs text-slate-800 block">Home</span>
              <span className="text-[10px] text-slate-500">STP O&amp;M Services</span>
            </div>
          </Link>

          <Link
            href="/schematic"
            className="p-3.5 rounded-xl bg-white border border-sky-100 hover:border-sky-300 shadow-xs hover:shadow-md transition-all group flex flex-col justify-between"
          >
            <div className="w-8 h-8 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center mb-2 group-hover:bg-sky-600 group-hover:text-white transition-colors">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <span className="font-bold text-xs text-slate-800 block">SCADA Mimic</span>
              <span className="text-[10px] text-slate-500">2.5D Digital Twin</span>
            </div>
          </Link>
        </div>

        {/* Back to Home Button */}
        <div className="pt-4">
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold shadow-md hover:shadow-lg transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Homepage</span>
          </Link>
        </div>
      </div>
    </div>
  )
}
