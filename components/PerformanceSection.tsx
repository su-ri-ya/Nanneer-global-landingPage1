"use client"

import React, { useState, useEffect, useRef } from "react"
import Image from "next/image"
import { motion, useInView } from "framer-motion"
import {
  Droplet,
  Settings,
  Users,
  FileText,
  Calendar,
  Building2,
  Gauge,
  Check,
  ArrowRight,
  MessageSquare,
} from "lucide-react"

interface PerformanceSectionProps {
  onOpenReportModal?: () => void
}

export function PerformanceSection({ onOpenReportModal }: PerformanceSectionProps) {
  const sectionRef = useRef<HTMLElement>(null)
  const reportRef = useRef<HTMLDivElement>(null)
  const photoRef = useRef<HTMLDivElement>(null)
  const ctaRef = useRef<HTMLButtonElement>(null)

  const isInView = useInView(sectionRef, { once: true, margin: "-60px" })

  // Interactive animated count-up states
  const [counts, setCounts] = useState({
    target: 0,
    influent: 0,
    treated: 0,
    recycled: 0,
    reuse: 0,
    avail: 0,
  })

  // Smooth Count-Up Animation (easeOutQuart)
  useEffect(() => {
    if (!isInView) return

    const duration = 1400
    const start = performance.now()
    let animationFrameId: number

    const easeOutQuart = (x: number): number => 1 - Math.pow(1 - x, 4)

    const tick = (now: number) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      const factor = easeOutQuart(progress)

      setCounts({
        target: Math.round(99 * factor),
        influent: Math.round(14850 * factor),
        treated: Math.round(14713 * factor),
        recycled: Math.round(14566 * factor),
        reuse: parseFloat((99.0 * factor).toFixed(1)),
        avail: parseFloat((99.4 * factor).toFixed(1)),
      })

      if (progress < 1) {
        animationFrameId = requestAnimationFrame(tick)
      }
    }

    animationFrameId = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(animationFrameId)
  }, [isInView])

  // Mouse & Pointer Interactions: Spotlight, Parallax, 3D Tilt, Magnetic CTA
  useEffect(() => {
    const sec = sectionRef.current
    if (!sec) return

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches

    const onPointerMove = (e: PointerEvent) => {
      const rect = sec.getBoundingClientRect()
      const x = ((e.clientX - rect.left) / rect.width) * 100
      const y = ((e.clientY - rect.top) / rect.height) * 100
      sec.style.setProperty("--mx", `${x.toFixed(2)}%`)
      sec.style.setProperty("--my", `${y.toFixed(2)}%`)

      if (prefersReducedMotion) return

      // Photo Parallax micro-shift
      if (photoRef.current) {
        const nx = (e.clientX - rect.left) / rect.width - 0.5
        const ny = (e.clientY - rect.top) / rect.height - 0.5
        photoRef.current.style.transform = `translate3d(${nx * 8}px, ${ny * 8}px, 0) scale(1.02)`
      }

      // 3D Report Card Tilt on hover
      if (reportRef.current) {
        const rRect = reportRef.current.getBoundingClientRect()
        const rx = (e.clientX - rRect.left) / rRect.width - 0.5
        const ry = (e.clientY - rRect.top) / rRect.height - 0.5
        const isInside = rx >= -0.5 && rx <= 0.5 && ry >= -0.5 && ry <= 0.5

        if (isInside) {
          const rotX = -ry * 5
          const rotY = rx * 5
          reportRef.current.style.transform = `perspective(1200px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) translateZ(4px)`
        } else {
          reportRef.current.style.transform = `perspective(1200px) rotateX(0deg) rotateY(0deg) translateZ(0)`
        }
      }

      // Magnetic CTA Button Pull
      if (ctaRef.current) {
        const ctaRect = ctaRef.current.getBoundingClientRect()
        const cx = e.clientX - (ctaRect.left + ctaRect.width / 2)
        const cy = e.clientY - (ctaRect.top + ctaRect.height / 2)
        const dist = Math.hypot(cx, cy)
        if (dist < 80) {
          ctaRef.current.style.transform = `translate3d(${cx * 0.15}px, ${cy * 0.15}px, 0)`
        } else {
          ctaRef.current.style.transform = `translate3d(0, 0, 0)`
        }
      }
    }

    const onPointerLeave = () => {
      if (reportRef.current) {
        reportRef.current.style.transform = `perspective(1200px) rotateX(0deg) rotateY(0deg) translateZ(0)`
      }
      if (photoRef.current) {
        photoRef.current.style.transform = `translate3d(0, 0, 0) scale(1)`
      }
      if (ctaRef.current) {
        ctaRef.current.style.transform = `translate3d(0, 0, 0)`
      }
    }

    sec.addEventListener("pointermove", onPointerMove)
    sec.addEventListener("pointerleave", onPointerLeave)

    return () => {
      sec.removeEventListener("pointermove", onPointerMove)
      sec.removeEventListener("pointerleave", onPointerLeave)
    }
  }, [])

  // Metric targets data
  const statTargets = [
    {
      icon: <Droplet className="w-4 h-4 text-emerald-600 fill-emerald-600" />,
      label: "Sewage Treatment Target",
      isHighlighted: false,
    },
    {
      icon: <Settings className="w-4 h-4 text-emerald-600 stroke-2" />,
      label: "STP Availability Target",
      isHighlighted: true,
    },
    {
      icon: <Users className="w-4 h-4 text-emerald-600 stroke-2" />,
      label: "Manpower Coverage Target",
      isHighlighted: false,
    },
  ]

  // Data for report card modules
  const waterBalanceData = [
    { label: "Influent (Sewage)", value: counts.influent.toLocaleString() },
    { label: "Treated Water", value: counts.treated.toLocaleString() },
    { label: "Recycled / Reused", value: counts.recycled.toLocaleString() },
  ]

  const waterQualityData = [
    { param: "pH", result: "7.2", standard: "6.5 – 8.5" },
    { param: "BOD (mg/L)", result: "6", standard: "≤ 10" },
    { param: "COD (mg/L)", result: "28", standard: "≤ 50" },
  ]

  const equipmentData = [
    { name: "Feed Pumps", value: "99.6%", width: 99.6 },
    { name: "Aeration Blowers", value: "99.2%", width: 99.2 },
    { name: "RAS / WAS Pumps", value: "99.5%", width: 99.5 },
  ]

  const maintenanceRecords = [
    "Daily checks – Completed (100%)",
    "Weekly activities – Completed (100%)",
    "Preventive maintenance – Completed as scheduled",
  ]

  const shiftData = [
    { shift: "Shift A (06:00 – 14:00)", coverage: "100%" },
    { shift: "Shift B (14:00 – 22:00)", coverage: "100%" },
    { shift: "Shift C (22:00 – 06:00)", coverage: "100%" },
  ]

  const videoEvidence = [
    { time: "08:30 AM", thumb: "/images/crops/solution_op.jpg" },
    { time: "01:15 PM", thumb: "/images/crops/solution_water.jpg" },
    { time: "05:00 PM", thumb: "/images/crops/solution_digital.jpg" },
  ]

  return (
    <section
      ref={sectionRef}
      id="performance"
      className="min-h-[calc(100vh-72px)] flex flex-col justify-center w-full blueprint-grid relative overflow-hidden bg-gradient-to-b from-white via-sky-50/40 to-white text-slate-900 py-8 sm:py-12 lg:py-8 px-3 sm:px-6 lg:px-8 border-t border-sky-100"
      style={{ ["--mx" as any]: "50%", ["--my" as any]: "50%" }}
    >
      {/* 1. Interactive Cursor Spotlight */}
      <div
        className="absolute inset-0 pointer-events-none transition-opacity duration-300 transform-gpu"
        style={{
          background: "radial-gradient(650px circle at var(--mx) var(--my), rgba(14, 165, 233, 0.2), transparent 70%)",
        }}
        aria-hidden="true"
      />

      {/* Decorative ambient curves */}
      <div className="absolute -bottom-16 -right-16 w-80 h-80 bg-sky-200/65 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" aria-hidden="true" />
      <div className="absolute -top-16 -left-16 w-72 h-72 bg-cyan-200/55 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" aria-hidden="true" />

      <div className="max-w-[1400px] mx-auto w-full relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-5 lg:gap-8 items-center">
        {/* ================= LEFT COLUMN ================= */}
        <motion.div
          className="lg:col-span-5 flex flex-col gap-2.5 sm:gap-3"
          initial={{ opacity: 0, x: -16 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Top Pill / Kicker with hover glow */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-50/90 border border-sky-200/80 w-fit shadow-2xs hover:border-sky-400 hover:shadow-xs transition-all duration-300 cursor-default">
            <span className="w-4 h-0.5 bg-sky-500 rounded-full" />
            <span className="font-mono text-[9px] sm:text-[10.5px] font-bold text-sky-700 tracking-wider uppercase">
              STP OPERATIONS &amp; MAINTENANCE FOR COMMERCIAL BUILDINGS
            </span>
          </div>

          {/* Heading with Mask Slide-up & Continuous Sheen */}
          <h2 className="font-display text-xl sm:text-3xl lg:text-[32px] font-extrabold tracking-tight leading-[1.15]">
            <span className="overflow-hidden block">
              <motion.span
                className="text-[#0B2545] block"
                initial={{ y: "100%" }}
                animate={isInView ? { y: 0 } : {}}
                transition={{ duration: 0.6, ease: [0.2, 0.8, 0.2, 1] }}
              >
                Performance You Can Measure.
              </motion.span>
            </span>
            <span className="overflow-hidden block mt-0.5">
              <motion.span
                className="block text-transparent bg-clip-text bg-gradient-to-r from-sky-600 via-sky-400 to-cyan-600 animate-shimmer"
                style={{
                  backgroundSize: "200% auto",
                }}
                initial={{ y: "100%" }}
                animate={isInView ? { y: 0 } : {}}
                transition={{ duration: 0.6, delay: 0.1, ease: [0.2, 0.8, 0.2, 1] }}
              >
                Operations You Can Verify.
              </motion.span>
            </span>
          </h2>

          {/* Subtitle */}
          <p className="text-xs sm:text-[13px] text-slate-600 leading-relaxed max-w-xl">
            We manage your STP 24×7 to maximize sewage treatment, recover reusable water,
            prevent operational failures, and keep every activity documented.
          </p>

          {/* 3 Metric Target Cards with Hover Lift & Glow */}
          <div className="grid grid-cols-3 gap-1.5 sm:gap-3 pt-0.5">
            {statTargets.map((stat, idx) => (
              <motion.div
                key={idx}
                whileHover={{ y: -3, scale: 1.02, transition: { duration: 0.2 } }}
                className={`rounded-xl p-1.5 sm:p-3 flex flex-col items-center text-center transition-all duration-300 relative group cursor-pointer ${
                  stat.isHighlighted
                    ? "bg-sky-50/80 border-2 border-sky-400 shadow-md shadow-sky-100 hover:border-sky-500 hover:shadow-lg hover:shadow-sky-200"
                    : "bg-white border border-sky-200/80 hover:border-sky-400 hover:shadow-md hover:shadow-sky-100 shadow-xs"
                }`}
              >
                {/* Gradient underline highlight on hover */}
                <div className="absolute bottom-0 inset-x-2 h-0.5 bg-gradient-to-r from-sky-500 to-cyan-400 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 rounded-full" />
                <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-emerald-50 border border-emerald-200/70 flex items-center justify-center mb-1 group-hover:scale-110 transition-transform duration-300">
                  {stat.icon}
                </div>
                <div className="text-sm sm:text-xl font-display font-extrabold text-[#0B2545] tracking-tight leading-none font-mono">
                  &ge;{counts.target}%
                </div>
                <div className="text-[9px] sm:text-[10.5px] font-semibold text-slate-700 mt-1 leading-tight">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>

          {/* Plant Photo with Parallax & Pulsing Live Radar Badge */}
          <div className="relative w-full h-[140px] sm:h-[160px] lg:h-[165px] rounded-xl overflow-hidden border border-sky-200/90 bg-slate-100 shadow-md group">
            <div ref={photoRef} className="absolute inset-[-4px] transition-transform duration-200 ease-out">
              <Image
                src="/images/crops/perf_plant.jpg"
                alt="STP Sewage Treatment Plant Operations"
                fill
                sizes="(max-width: 1024px) 100vw, 45vw"
                className="object-cover transition-transform duration-700 ease-out group-hover:scale-106"
              />
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-black/45 via-transparent to-transparent pointer-events-none" />
            
            {/* Live Status Badge with Radar Ping */}
            <div className="absolute bottom-2.5 left-2.5 bg-white/95 backdrop-blur-md px-2.5 py-1 rounded-full border border-sky-200 shadow-sm flex items-center gap-1.5 transition-transform duration-300 group-hover:scale-105">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
              </span>
              <span className="text-[9px] font-mono font-bold text-slate-800 uppercase tracking-wider">
                Clarification Tank Verified
              </span>
            </div>
          </div>
        </motion.div>

        {/* ================= RIGHT COLUMN: INTERACTIVE REPORT CARD ================= */}
        <motion.div
          className="lg:col-span-7 flex flex-col"
          initial={{ opacity: 0, x: 16 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.5, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Main Card Container with 3D Tilt */}
          <div
            ref={reportRef}
            className="rounded-2xl border border-slate-200/90 shadow-xl bg-white overflow-hidden transition-transform duration-200 ease-out relative"
            style={{ transformStyle: "preserve-3d" }}
          >
            {/* Header Glint Sweep Effect */}
            <div className="absolute top-0 left-[-100%] w-1/2 h-14 bg-gradient-to-r from-transparent via-white/15 to-transparent skew-x-[-20deg] pointer-events-none animate-glint" />

            {/* Brand Sky Blue Header */}
            <div className="bg-gradient-to-r from-sky-600 via-sky-700 to-sky-800 text-white p-3 sm:p-3.5 flex items-center justify-between border-b border-sky-500/30 relative z-10 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-white/10 border border-white/20 flex items-center justify-center text-sky-200 shadow-inner group-hover:scale-105 transition-transform">
                  <FileText className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h3 className="font-display text-sm sm:text-base font-bold text-white tracking-tight leading-snug">
                    Monthly STP Performance Report
                  </h3>
                  <p className="text-[10.5px] text-sky-200/90 leading-tight">
                    STP Operations &amp; Maintenance | Monthly Management Report
                  </p>
                </div>
              </div>

              {/* Nanneer Global Brand Pill */}
              <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white/10 border border-white/20 text-white font-mono text-[9.5px] sm:text-[10px] font-bold tracking-wider hover:bg-white/15 transition-colors cursor-default">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_6px_#10b981]" />
                <span>NANNEER GLOBAL</span>
              </div>
            </div>

            {/* Clean Light Metadata Bar */}
            <div className="bg-slate-50 border-b border-slate-200/80 px-3.5 sm:px-4 py-2 flex flex-wrap items-center justify-between gap-2 font-mono text-[10px] sm:text-[11px] text-slate-600">
              <span className="flex items-center gap-1.5 hover:text-sky-700 transition-colors">
                <Calendar className="w-3.5 h-3.5 text-sky-600" />
                Report Period: Aug 2025
              </span>
              <span className="flex items-center gap-1.5 hover:text-sky-700 transition-colors">
                <Building2 className="w-3.5 h-3.5 text-sky-600" />
                Building: Commercial Office
              </span>
              <span className="flex items-center gap-1.5 hover:text-sky-700 transition-colors">
                <Gauge className="w-3.5 h-3.5 text-sky-600" />
                STP Capacity: 500 KLD
              </span>
            </div>

            {/* 6 Structured Modules with Hover Elevation */}
            <div className="p-3 sm:p-3.5 grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 bg-slate-50/30">
              {/* Module 1: Water Balance */}
              <div className="rounded-xl border border-slate-200/80 bg-white p-2.5 sm:p-3 flex flex-col justify-between shadow-2xs hover:border-sky-300 hover:shadow-xs hover:-translate-y-0.5 transition-all duration-300">
                <div>
                  <div className="font-display font-bold text-[11px] sm:text-xs text-slate-800 flex items-center gap-1.5 mb-2">
                    <FileText className="w-3.5 h-3.5 text-sky-600" />
                    <span>1. Water Balance (KLD)</span>
                  </div>
                  <div className="space-y-1 text-[10.5px] sm:text-[11px]">
                    {waterBalanceData.map((row, idx) => (
                      <div key={idx} className="flex justify-between items-center text-slate-600">
                        <span>{row.label}</span>
                        <span className="font-mono font-bold text-slate-900">{row.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="mt-2 pt-1.5 border-t border-slate-100 flex items-center justify-between text-[10.5px] sm:text-[11px]">
                  <span className="text-emerald-700 font-semibold">Treatment &amp; Reuse</span>
                  <span className="font-mono font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200 text-[10px]">
                    {counts.reuse.toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Module 2: Treated-Water Quality with Popping Check Badges */}
              <div className="rounded-xl border border-slate-200/80 bg-white p-2.5 sm:p-3 shadow-2xs hover:border-sky-300 hover:shadow-xs hover:-translate-y-0.5 transition-all duration-300">
                <div className="font-display font-bold text-[11px] sm:text-xs text-slate-800 flex items-center gap-1.5 mb-1.5">
                  <Droplet className="w-3.5 h-3.5 text-sky-600 fill-sky-600" />
                  <span>2. Treated-Water Quality (Avg.)</span>
                </div>
                <div className="text-[9px] sm:text-[10.5px]">
                  <div className="grid grid-cols-4 gap-1 text-slate-500 font-mono pb-1 border-b border-slate-100">
                    <span>Parameter</span>
                    <span className="text-right">Result</span>
                    <span className="text-right">Standard</span>
                    <span className="text-center">Status</span>
                  </div>
                  <div className="space-y-1 pt-1">
                    {waterQualityData.map((row, idx) => (
                      <div key={idx} className="grid grid-cols-4 gap-1 items-center text-slate-600">
                        <span className="font-medium text-slate-800">{row.param}</span>
                        <span className="text-right font-mono font-bold text-slate-900">{row.result}</span>
                        <span className="text-right font-mono text-slate-500">{row.standard}</span>
                        <div className="flex justify-center">
                          <motion.span
                            initial={{ scale: 0 }}
                            animate={isInView ? { scale: 1 } : {}}
                            transition={{
                              type: "spring",
                              stiffness: 300,
                              damping: 18,
                              delay: 0.3 + idx * 0.08,
                            }}
                            className="w-3.5 h-3.5 rounded-full bg-emerald-500 text-white flex items-center justify-center shadow-2xs"
                          >
                            <Check className="w-2 h-2 stroke-[3]" />
                          </motion.span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Module 3: Equipment Performance with Animated Progress Bars */}
              <div className="rounded-xl border border-slate-200/80 bg-white p-2.5 sm:p-3 shadow-2xs hover:border-sky-300 hover:shadow-xs hover:-translate-y-0.5 transition-all duration-300">
                <div className="font-display font-bold text-[11px] sm:text-xs text-slate-800 flex items-center gap-1.5 mb-2">
                  <Settings className="w-3.5 h-3.5 text-sky-600 stroke-2" />
                  <span>3. Equipment Performance</span>
                </div>
                <div className="space-y-1.5 text-[10.5px] sm:text-[11px]">
                  {equipmentData.map((eq, idx) => (
                    <div key={idx}>
                      <div className="flex justify-between items-center text-slate-600 mb-0.5">
                        <span>{eq.name}</span>
                        <span className="font-mono font-bold text-slate-900">{eq.value}</span>
                      </div>
                      <div className="w-full h-1 rounded-full bg-slate-100 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full bg-gradient-to-r from-sky-500 to-cyan-500"
                          initial={{ width: 0 }}
                          animate={isInView ? { width: `${eq.width}%` } : {}}
                          transition={{ duration: 1.2, delay: 0.2 + idx * 0.1, ease: [0.2, 0.8, 0.2, 1] }}
                        />
                      </div>
                    </div>
                  ))}
                  <div className="pt-1.5 border-t border-slate-100 flex justify-between items-center text-slate-800 font-semibold text-[10.5px]">
                    <span>Overall Availability</span>
                    <span className="font-mono font-bold text-sky-600">{counts.avail.toFixed(1)}%</span>
                  </div>
                </div>
              </div>

              {/* Module 4: Maintenance Records */}
              <div className="rounded-xl border border-slate-200/80 bg-white p-2.5 sm:p-3 shadow-2xs hover:border-sky-300 hover:shadow-xs hover:-translate-y-0.5 transition-all duration-300">
                <div className="font-display font-bold text-[11px] sm:text-xs text-slate-800 flex items-center gap-1.5 mb-2">
                  <Check className="w-3.5 h-3.5 text-sky-600 stroke-[3]" />
                  <span>4. Maintenance Records</span>
                </div>
                <div className="space-y-1.5 text-[10.5px] sm:text-[11px]">
                  {maintenanceRecords.map((record, idx) => (
                    <div key={idx} className="flex items-start gap-1.5 text-slate-600">
                      <Check className="w-3 h-3 text-emerald-500 stroke-[3] shrink-0 mt-0.5" />
                      <span className="leading-tight">{record}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Module 5: Manpower Coverage */}
              <div className="rounded-xl border border-slate-200/80 bg-white p-2.5 sm:p-3 shadow-2xs hover:border-sky-300 hover:shadow-xs hover:-translate-y-0.5 transition-all duration-300">
                <div className="font-display font-bold text-[11px] sm:text-xs text-slate-800 flex items-center gap-1.5 mb-2">
                  <Users className="w-3.5 h-3.5 text-sky-600 stroke-2" />
                  <span>5. Manpower Coverage</span>
                </div>
                <div className="text-[10px] sm:text-[10.5px]">
                  <div className="flex justify-between text-slate-500 font-mono pb-1 border-b border-slate-100">
                    <span>Shift</span>
                    <span>Coverage</span>
                  </div>
                  <div className="space-y-1 pt-1">
                    {shiftData.map((shift, idx) => (
                      <div key={idx} className="flex justify-between items-center text-slate-600">
                        <span>{shift.shift}</span>
                        <span className="font-mono font-bold text-slate-900">{shift.coverage}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Module 6: WhatsApp Evidence with Gallery Hover Focus */}
              <div className="rounded-xl border border-slate-200/80 bg-white p-2.5 sm:p-3 shadow-2xs hover:border-sky-300 hover:shadow-xs hover:-translate-y-0.5 transition-all duration-300">
                <div className="font-display font-bold text-[11px] sm:text-xs text-slate-800 flex items-center gap-1.5 mb-2">
                  <MessageSquare className="w-3.5 h-3.5 text-sky-600" />
                  <span>6. WhatsApp Communication Evidence</span>
                </div>
                <div className="grid grid-cols-3 gap-1.5 group/gallery">
                  {videoEvidence.map((vid, idx) => (
                    <div
                      key={idx}
                      onClick={onOpenReportModal}
                      className="relative aspect-[16/10] rounded-md overflow-hidden border border-slate-200 bg-slate-100 cursor-pointer transition-all duration-300 group/vid group-hover/gallery:opacity-60 hover:!opacity-100 hover:scale-108 hover:z-10 hover:shadow-md hover:border-sky-400"
                    >
                      <Image
                        src={vid.thumb}
                        alt="WhatsApp daily operational log evidence"
                        fill
                        sizes="80px"
                        className="object-cover transition-transform duration-300 group-hover/vid:scale-110"
                      />
                      <div className="absolute bottom-0.5 right-0.5 px-1 rounded bg-black/70 backdrop-blur-2xs font-mono text-[7px] text-white">
                        {vid.time}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Bottom Magnetic CTA Button with Light Wave */}
            <div className="p-3 sm:p-3.5 pt-1.5 bg-white">
              <button
                ref={ctaRef}
                type="button"
                onClick={onOpenReportModal}
                className="w-full py-2.5 sm:py-3 rounded-full bg-gradient-to-r from-sky-600 to-sky-700 hover:from-sky-700 hover:to-sky-800 text-white font-display font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all duration-200 shadow-md shadow-sky-600/20 hover:shadow-sky-600/35 relative overflow-hidden group cursor-pointer"
              >
                {/* Wave effect across button on hover */}
                <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
                <span className="relative z-10 flex items-center gap-2">
                  <span>Request Sample Performance Report</span>
                  <ArrowRight className="w-3.5 h-3.5 stroke-[2.5] transition-transform duration-300 group-hover:translate-x-1.5" />
                </span>
              </button>
            </div>
          </div>
        </motion.div>
      </div>

      <style jsx>{`
        @keyframes glint {
          0%, 75% { left: -100%; }
          100% { left: 200%; }
        }
        .animate-glint {
          animation: glint 10s infinite;
        }
        @keyframes shimmer {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
        .animate-shimmer {
          animation: shimmer 6s linear infinite;
        }
      `}</style>
    </section>
  )
}
