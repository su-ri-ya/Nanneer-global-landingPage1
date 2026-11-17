"use client"

import React from "react"
import Link from "next/link"
import { ScadaSchematicSimulation } from "@/components/ScadaSchematicSimulation"
import { PumpConceptShowcase } from "@/components/PumpConceptShowcase"
import { ArrowLeft } from "lucide-react"

export default function SchematicPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col p-2 sm:p-4 md:p-6 font-sans selection:bg-sky-200 selection:text-sky-950">
      <div className="max-w-[1300px] mx-auto w-full mb-3 flex items-center justify-between">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-sky-50 text-slate-700 hover:text-sky-900 text-xs font-semibold transition-colors border border-sky-200/80 shadow-xs"
        >
          <ArrowLeft className="w-3.5 h-3.5 text-sky-600" />
          <span>Back to Home</span>
        </Link>
      </div>

      <main className="max-w-[1300px] mx-auto w-full flex-1 flex flex-col">
        <ScadaSchematicSimulation />
        <PumpConceptShowcase />
      </main>
    </div>
  )
}
