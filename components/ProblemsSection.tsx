"use client"

import React from "react"
import { Droplet, AlertTriangle, ClipboardList, Users } from "lucide-react"

export function ProblemsSection() {
  const problems = [
    {
      title: "Water Wastage",
      description: "Treated water not fully utilized.",
      icon: Droplet,
      accent: "text-cyan-600 bg-cyan-50 border-cyan-100",
      borderHover: "hover:border-cyan-300",
    },
    {
      title: "Unexpected Incidents",
      description: "Overflows, breakdowns and complaints.",
      icon: AlertTriangle,
      accent: "text-amber-600 bg-amber-50 border-amber-100",
      borderHover: "hover:border-amber-300",
    },
    {
      title: "Poor Documentation",
      description: "Incomplete logs and missing records.",
      icon: ClipboardList,
      accent: "text-emerald-600 bg-emerald-50 border-emerald-100",
      borderHover: "hover:border-emerald-300",
    },
    {
      title: "Manpower Dependency",
      description: "Constant supervision and follow-ups.",
      icon: Users,
      accent: "text-teal-600 bg-teal-50 border-teal-100",
      borderHover: "hover:border-teal-300",
    },
  ]

  return (
    <section id="why-nanneer" className="py-20 bg-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Heading */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <div className="inline-block w-12 h-1 bg-teal-600 rounded-full mb-4" />
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Managing an STP Shouldn&apos;t Be a Daily Headache.
          </h2>
          <p className="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed font-normal">
            You have enough responsibilities managing your building. Your STP should not
            require constant follow-ups, unexpected interventions, or last-minute
            preparation for inspections.
          </p>
        </div>

        {/* 4 Problem Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {problems.map((item, idx) => {
            const Icon = item.icon
            return (
              <div
                key={idx}
                className={`p-6 sm:p-7 rounded-2xl bg-slate-50/80 border border-slate-200/90 shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 ${item.borderHover} flex flex-col justify-between`}
              >
                <div>
                  <div
                    className={`w-14 h-14 rounded-xl flex items-center justify-center border mb-6 ${item.accent}`}
                  >
                    <Icon className="w-7 h-7" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">
                    {item.title}
                  </h3>
                  <p className="text-sm sm:text-base text-slate-600 leading-normal">
                    {item.description}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-200/60 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                  <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Eliminated by Nanneer
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

