"use client"

import React, { useState, useEffect } from "react"
import Link from "next/link"
import Image from "next/image"
import {
  ChevronLeft,
  ChevronRight,
  Download,
  Home,
  Droplets,
  HardHat,
  Laptop,
  Settings,
  Users,
  ShieldCheck,
  FileText,
} from "lucide-react"

export default function PresentationPage() {
  const [currentSlide, setCurrentSlide] = useState(0)

  const slides = [
    {
      id: "screen1",
      tag: "Screen 01 · Hero & Pain Points",
      title: "Your STP Is Running. But Is It Delivering?",
      subtitle: "STP Operations & Maintenance for Commercial Buildings",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center h-full">
          <div className="md:col-span-7 space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F5F3] text-[#006778] text-xs font-bold uppercase tracking-wider">
              <span>Screen 1 / 4 · Core Value Proposition</span>
            </div>
            <h1 className="text-3xl sm:text-5xl font-black text-[#0D263B] tracking-tight leading-tight">
              Your STP Is Running.
              <br />
              <span className="text-[#006778]">But Is It Delivering?</span>
            </h1>
            <p className="text-sm sm:text-base text-slate-600 leading-relaxed max-w-lg">
              We manage your STP 24×7 to maximize sewage treatment, recover reusable water,
              prevent operational failures, and keep every activity documented.
            </p>
            <p className="text-sm font-extrabold text-[#0D263B]">
              Not just manpower. Complete operational accountability.
            </p>
            <div className="grid grid-cols-2 gap-2 pt-2 text-xs">
              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800">Water Wastage</span>
                <p className="text-slate-500">Treated water not fully utilized.</p>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800">Unexpected Incidents</span>
                <p className="text-slate-500">Overflows, breakdowns &amp; complaints.</p>
              </div>
            </div>
          </div>

          <div className="md:col-span-5 relative h-64 sm:h-80 rounded-2xl overflow-hidden shadow-xl border border-slate-200">
            <Image
              src="/images/crops/hero_plant.jpg"
              alt="STP Operations"
              fill
              className="object-cover"
            />
          </div>
        </div>
      ),
    },
    {
      id: "screen2",
      tag: "Screen 02 · The Solution (3 Pillars)",
      title: "One Partner. Complete STP Responsibility.",
      subtitle: "From operator deployment to water recovery and monthly reporting",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-3">
            <div className="relative h-36 rounded-xl overflow-hidden">
              <Image
                src="/images/crops/solution_op.jpg"
                alt="24x7 Operations"
                fill
                className="object-cover"
              />
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#E8F5F3] text-[#006778] flex items-center justify-center">
                <HardHat className="w-4 h-4" />
              </div>
              <h3 className="text-base font-bold text-[#0D263B]">24×7 Operations</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Trained operators across three shifts, supported by defined SOPs, supervision,
              and preventive maintenance.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-3">
            <div className="relative h-36 rounded-xl overflow-hidden">
              <Image
                src="/images/crops/solution_water.jpg"
                alt="Maximum Water Recovery"
                fill
                className="object-cover"
              />
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#E8F5F3] text-[#006778] flex items-center justify-center">
                <Droplets className="w-4 h-4" />
              </div>
              <h3 className="text-base font-bold text-[#0D263B]">Water Recovery</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Measure, treat, and maximize safe reuse of wastewater for cooling towers,
              toilet flushing, and gardening.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-3">
            <div className="relative h-36 rounded-xl overflow-hidden">
              <Image
                src="/images/crops/solution_digital.jpg"
                alt="Digital Monitoring"
                fill
                className="object-cover"
              />
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#E8F5F3] text-[#006778] flex items-center justify-center">
                <Laptop className="w-4 h-4" />
              </div>
              <h3 className="text-base font-bold text-[#0D263B]">Digital Monitoring</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Track water quantity, quality, tank levels, equipment health, and scheduled
              activities with documented evidence.
            </p>
          </div>
        </div>
      ),
    },
    {
      id: "screen3",
      tag: "Screen 03 · Verifiable Performance",
      title: "Performance You Can Measure. Operations You Can Verify.",
      subtitle: "Measurable Targets & Transparent Monthly Management Report",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          <div className="md:col-span-5 space-y-3">
            <div className="p-3.5 rounded-xl bg-teal-50/70 border border-teal-100">
              <div className="text-2xl font-black text-[#006778]">&ge;99%</div>
              <div className="text-xs font-bold text-slate-800">Sewage Treatment Target</div>
            </div>
            <div className="p-3.5 rounded-xl bg-teal-50/70 border border-teal-100">
              <div className="text-2xl font-black text-[#006778]">&ge;99%</div>
              <div className="text-xs font-bold text-slate-800">STP Availability Target</div>
            </div>
            <div className="p-3.5 rounded-xl bg-teal-50/70 border border-teal-100">
              <div className="text-2xl font-black text-[#006778]">&ge;99%</div>
              <div className="text-xs font-bold text-slate-800">Manpower Coverage Target</div>
            </div>
          </div>

          <div className="md:col-span-7 rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-3 text-xs">
            <div className="bg-[#0E293E] text-white p-3 rounded-xl flex items-center justify-between">
              <div>
                <div className="font-bold">Monthly STP Performance Report</div>
                <div className="text-[10px] text-slate-300">Aug 2025 · Commercial Office · 500 KLD</div>
              </div>
              <div className="text-[10px] font-bold text-teal-300 font-mono">NANNEER GLOBAL</div>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="p-2.5 bg-slate-50 rounded-lg">
                <span className="font-bold text-slate-800">1. Water Balance</span>
                <div className="text-slate-600 mt-0.5">14,850 in / 14,566 reused (99.0%)</div>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg">
                <span className="font-bold text-slate-800">2. Water Quality</span>
                <div className="text-slate-600 mt-0.5">pH 7.2 · BOD 6 · COD 28 · TSS 8</div>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg">
                <span className="font-bold text-slate-800">3. Equipment</span>
                <div className="text-slate-600 mt-0.5">99.4% overall uptime</div>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg">
                <span className="font-bold text-slate-800">4. Manpower</span>
                <div className="text-slate-600 mt-0.5">Shift A, B, C 100% manned</div>
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      id: "screen4",
      tag: "Screen 04 · Facility Assessment & Inquiry",
      title: "Is Your STP Performing at Its Best?",
      subtitle: "Tailored Facility Diagnostic for Commercial Real Estate",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          <div className="md:col-span-5 relative h-64 sm:h-72 rounded-2xl overflow-hidden shadow-md border border-slate-200">
            <Image
              src="/images/crops/contact_plant.jpg"
              alt="STP Aeration Facility"
              fill
              className="object-cover"
            />
          </div>

          <div className="md:col-span-7 p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-xl font-black text-[#0D263B]">
              Ready for Reliable, Headache-Free STP Management?
            </h3>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Let&apos;s evaluate your current operating expenses, blower uptime, sludge
              management, and water reuse options. No complex technical documents required.
            </p>
            <div className="space-y-2 text-xs">
              <div className="p-2.5 bg-slate-50 rounded-lg flex items-center justify-between">
                <span className="font-semibold text-slate-700">Building Types Covered:</span>
                <span className="font-bold text-[#0D263B]">Commercial Office, IT Park, Hotel, Mall</span>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg flex items-center justify-between">
                <span className="font-semibold text-slate-700">Response SLA:</span>
                <span className="font-bold text-emerald-700">Direct Engineer Audit within 24h</span>
              </div>
            </div>
          </div>
        </div>
      ),
    },
  ]

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev < slides.length - 1 ? prev + 1 : prev))
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev > 0 ? prev - 1 : prev))
  }

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === " ") {
        nextSlide()
      } else if (e.key === "ArrowLeft") {
        prevSlide()
      }
    }
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [currentSlide])

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col font-sans select-none">
      {/* Top Bar */}
      <header className="bg-slate-900 border-b border-slate-800 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/"
            className="flex items-center gap-2 text-xs font-bold text-slate-300 hover:text-white px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 transition"
          >
            <Home className="w-3.5 h-3.5" />
            <span>Live Website</span>
          </Link>
          <span className="text-xs font-bold uppercase tracking-wider text-teal-400">
            Nanneer Global Deck
          </span>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={prevSlide}
            disabled={currentSlide === 0}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 transition"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <span className="text-xs font-mono font-bold">
            {currentSlide + 1} / {slides.length}
          </span>
          <button
            onClick={nextSlide}
            disabled={currentSlide === slides.length - 1}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 transition"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        <div>
          <a
            href="/Nanneer_Global_STP_Operations_Presentation.pptx"
            download
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#006778] hover:bg-[#005260] text-white text-xs font-bold transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download PPTX</span>
          </a>
        </div>
      </header>

      {/* Main Slide Canvas */}
      <main className="flex-1 flex items-center justify-center p-4 sm:p-8">
        <div className="w-full max-w-5xl aspect-[16/9] bg-white text-slate-900 rounded-3xl shadow-2xl border-4 border-slate-800 overflow-hidden flex flex-col p-6 sm:p-10 relative">
          {/* Slide Header */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <span className="text-xs font-bold uppercase tracking-wider text-[#006778]">
              {slides[currentSlide].tag}
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              NANNEER GLOBAL · DRAFT 3
            </span>
          </div>

          {/* Slide Body */}
          <div className="flex-1 py-4 flex flex-col justify-center">
            {slides[currentSlide].content}
          </div>

          {/* Slide Footer */}
          <div className="pt-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-400">
            <span>Confidence in Every Drop · 24×7 Operations &amp; Maintenance</span>
            <span className="font-mono">0{currentSlide + 1} / 0{slides.length}</span>
          </div>
        </div>
      </main>

      {/* Thumbnails bar */}
      <footer className="bg-slate-900 border-t border-slate-800 px-6 py-2.5 flex items-center justify-center gap-2">
        {slides.map((s, idx) => (
          <button
            key={s.id}
            onClick={() => setCurrentSlide(idx)}
            className={`px-3 py-1 rounded-md text-xs font-semibold transition ${
              currentSlide === idx
                ? "bg-[#006778] text-white"
                : "bg-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            {idx + 1}. {s.title.substring(0, 20)}...
          </button>
        ))}
      </footer>
    </div>
  )
}
