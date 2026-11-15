"use client"

import React, { useState } from "react"
import { Navbar } from "@/components/Navbar"
import { HeroSection } from "@/components/HeroSection"
import { SolutionSection } from "@/components/SolutionSection"
import { PerformanceSection } from "@/components/PerformanceSection"
import { AssessmentContactSection } from "@/components/AssessmentContactSection"
import { ReportModal } from "@/components/ReportModal"
import { Footer } from "@/components/Footer"

export default function Draft3HomePage() {
  const [reportModalOpen, setReportModalOpen] = useState(false)

  return (
    <div className="min-h-screen bg-white text-slate-900 selection:bg-sky-200 selection:text-sky-950 font-body">
      {/* 1. Fixed / Sticky Top Navbar */}
      <Navbar />

      <main className="divide-y divide-sky-100/80 scroll-smooth">
        {/* Screen 1: Hero & 4 Headache Cards */}
        <HeroSection onOpenReportModal={() => setReportModalOpen(true)} />

        {/* Screen 2: The Solution - 3 Modules */}
        <SolutionSection />

        {/* Screen 3: Performance Targets & Monthly Report Card */}
        <PerformanceSection onOpenReportModal={() => setReportModalOpen(true)} />

        {/* Screen 4: Assessment & Contact Form */}
        <AssessmentContactSection />

        {/* Footer */}
        <Footer />
      </main>

      {/* Interactive Monthly Report Modal */}
      <ReportModal
        isOpen={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
      />
    </div>
  )
}
