"use client"

import React from "react"
import Link from "next/link"
import { ScadaSchematicSimulation } from "@/components/ScadaSchematicSimulation"
import { ArrowLeft } from "lucide-react"

export default function SchematicPage() {
  return (
    <div className="h-screen max-h-screen bg-slate-50 flex flex-col p-1 sm:p-2 [@media(max-height:500px)]:p-0.5 overflow-hidden font-sans selection:bg-sky-200 selection:text-sky-950">
      <div className="w-full mb-1 [@media(max-height:500px)]:mb-0.5 shrink-0 flex items-center justify-between">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 px-2.5 py-1 [@media(max-height:500px)]:py-0.5 [@media(max-height:500px)]:px-2 rounded-lg bg-white hover:bg-sky-50 text-slate-700 hover:text-sky-900 text-xs [@media(max-height:500px)]:text-[10px] font-semibold transition-colors border border-sky-200/80 shadow-xs"
        >
          <ArrowLeft className="w-3.5 h-3.5 text-sky-600 [@media(max-height:500px)]:w-3 [@media(max-height:500px)]:h-3" />
          <span>Back to Home</span>
        </Link>
      </div>

      <main className="w-full flex-1 min-h-0 flex flex-col">
        <ScadaSchematicSimulation />
      </main>
    </div>
  )
}
