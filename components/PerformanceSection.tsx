"use client"

import React, { useState, useEffect, useRef } from "react"
import Image from "next/image"
import { motion, useInView, AnimatePresence } from "framer-motion"
import {
  Droplet,
  Settings,
  Users,
  FileText,
  Calendar,
  Building2,
  Gauge,
  ArrowRight,
  ZoomIn,
  ZoomOut,
  X,
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  TrendingUp,
  BarChart3,
  Layers,
  BookOpen,
  ShieldCheck,
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

  // Active Module State: 'water' (Pages 3 & 11) or 'tank' (Page 2)
  const [activeModule, setActiveModule] = useState<"water" | "tank">("water")

  // For Water Module: toggle between Page 3 and Page 11 on smaller screens, or both on wide
  const [activeWaterPage, setActiveWaterPage] = useState<3 | 11>(3)

  // Actual Report Registry for Lightbox
  const allSheets = [
    {
      id: "water-spc",
      pageBadge: "PAGE 03",
      title: "Water Consumption SPC Control Charts",
      subtitle: "30-Day Limits (UCL / LCL Bands) & Daily Anomaly Flags",
      docCategory: "Monthly Water Consumption Audit",
      image: "/images/reports/water_consumption_spc_p3.png",
      finding: "Real-time EMF flowmeter tracking with Statistical Process Control (SPC) bands to catch pipe leaks early, eliminate water loss, and verify daily sewage intake.",
    },
    {
      id: "mbbr-stability",
      pageBadge: "PAGE 11",
      title: "MBBR Inlet Process Stability Analysis",
      subtitle: "Coefficient of Variation (CV = 49.21%) & Statistical Dispersion",
      docCategory: "Biological Process Audit",
      image: "/images/reports/water_consumption_stability_p11.png",
      finding: "Measures biological process stability (CV 49.21%) so commercial facility managers can prevent shock loads and ensure consistent treated water quality.",
    },
    {
      id: "tank-levels",
      pageBadge: "PAGE 02",
      title: "Tank Level Control Charts & Breach Analytics",
      subtitle: "Continuous Volume Limits across Treated, Collection & Soft Water Tanks",
      docCategory: "Tank Volume & Level Audit",
      image: "/images/reports/tank_level_control_charts_p2.png",
      finding: "24×7 automated level monitoring across treated, collection, and soft water tanks to guarantee zero basement overflows and protect transfer pumps from running dry.",
    },
    {
      id: "tank-stability",
      pageBadge: "PAGE 05",
      title: "Treated Water Tank Process Stability Analysis",
      subtitle: "Coefficient of Variation (CV = 29.04%) & Daily Level Zones",
      docCategory: "Water Availability Audit",
      image: "/images/reports/tank_level_stability_p5.png",
      finding: "Proves 96.8% compliance in safe operating zones, ensuring your building always has continuous soft water for HVAC cooling towers and flush lines.",
    },
  ]

  // Active Lightbox Zoom State (image index 0 = p3, 1 = p11, 2 = p2, 3 = p5)
  const [zoomedPageIdx, setZoomedPageIdx] = useState<number | null>(null)
  const [zoomScale, setZoomScale] = useState<number>(1)
  const [panOffset, setPanOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 })
  const isDraggingRef = useRef(false)
  const hasDraggedRef = useRef(false)
  const dragStartRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 })
  const isWheelThrottled = useRef(false)
  const modalRef = useRef<HTMLDivElement>(null)

  // Reset zoom & pan whenever active page changes or modal closes
  useEffect(() => {
    setZoomScale(1)
    setPanOffset({ x: 0, y: 0 })
  }, [zoomedPageIdx])

  // Lock body scroll while lightbox is active so background website never scrolls
  useEffect(() => {
    if (zoomedPageIdx === null) return
    const originalOverflow = document.body.style.overflow
    document.body.style.overflow = "hidden"
    return () => {
      document.body.style.overflow = originalOverflow
    }
  }, [zoomedPageIdx])

  // Non-passive native wheel listener to isolate mouse wheel events inside the modal
  useEffect(() => {
    const el = modalRef.current
    if (!el || zoomedPageIdx === null) return

    const onWheelNative = (e: WheelEvent) => {
      e.preventDefault()
      e.stopPropagation()

      // Holding Ctrl/Cmd or pinch gesture: zoom in/out!
      if (e.ctrlKey || e.metaKey) {
        if (e.deltaY < 0) {
          setZoomScale((prev) => Math.min(2.5, +(prev + 0.25).toFixed(2)))
        } else {
          setZoomScale((prev) => {
            const next = Math.max(1, +(prev - 0.25).toFixed(2))
            if (next <= 1) setPanOffset({ x: 0, y: 0 })
            return next
          })
        }
        return
      }

      // If zoomed in (> 1), wheel scrolls/pans the document vertically
      if (zoomScale > 1) {
        setPanOffset((prev) => ({
          x: prev.x,
          y: Math.max(-550 * (zoomScale - 1), Math.min(550 * (zoomScale - 1), prev.y - e.deltaY * 0.9)),
        }))
        return
      }

      // If fit to screen (zoomScale === 1), wheel flips pages
      if (isWheelThrottled.current) return
      if (Math.abs(e.deltaY) < 18) return

      isWheelThrottled.current = true
      setTimeout(() => {
        isWheelThrottled.current = false
      }, 320)

      if (e.deltaY > 0) {
        setZoomedPageIdx((prev) => (prev !== null && prev < allSheets.length - 1 ? prev + 1 : 0))
      } else {
        setZoomedPageIdx((prev) => (prev !== null && prev > 0 ? prev - 1 : allSheets.length - 1))
      }
    }

    el.addEventListener("wheel", onWheelNative, { passive: false })
    return () => el.removeEventListener("wheel", onWheelNative)
  }, [zoomedPageIdx, zoomScale, allSheets.length])

  // Pan / Drag Handlers for Zoomed Document
  const handleMouseDown = (e: React.MouseEvent) => {
    isDraggingRef.current = true
    hasDraggedRef.current = false
    dragStartRef.current = { x: e.clientX - panOffset.x, y: e.clientY - panOffset.y }
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDraggingRef.current) return
    const dx = e.clientX - dragStartRef.current.x - panOffset.x
    const dy = e.clientY - dragStartRef.current.y - panOffset.y
    if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {
      hasDraggedRef.current = true
    }
    if (zoomScale <= 1) return
    const maxPanX = 350 * (zoomScale - 1)
    const maxPanY = 550 * (zoomScale - 1)
    setPanOffset({
      x: Math.max(-maxPanX, Math.min(maxPanX, e.clientX - dragStartRef.current.x)),
      y: Math.max(-maxPanY, Math.min(maxPanY, e.clientY - dragStartRef.current.y)),
    })
  }

  const handleMouseUp = () => {
    isDraggingRef.current = false
  }

  const toggleZoom = (e?: React.MouseEvent) => {
    if (e) e.stopPropagation()
    if (hasDraggedRef.current) return
    if (zoomScale > 1) {
      setZoomScale(1)
      setPanOffset({ x: 0, y: 0 })
    } else {
      setZoomScale(1.8)
    }
  }

  // Keyboard Navigation for Lightbox (Arrow Keys, Zoom +, -, 0, Escape)
  useEffect(() => {
    if (zoomedPageIdx === null) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setZoomedPageIdx(null)
      if (e.key === "ArrowRight" || e.key === "PageDown") {
        setZoomedPageIdx((prev) => (prev !== null && prev < allSheets.length - 1 ? prev + 1 : 0))
      }
      if (e.key === "ArrowLeft" || e.key === "PageUp") {
        setZoomedPageIdx((prev) => (prev !== null && prev > 0 ? prev - 1 : allSheets.length - 1))
      }
      if (e.key === "+" || e.key === "=") {
        setZoomScale((prev) => Math.min(2.5, +(prev + 0.3).toFixed(1)))
      }
      if (e.key === "-" || e.key === "_") {
        setZoomScale((prev) => {
          const next = Math.max(1, +(prev - 0.3).toFixed(1))
          if (next <= 1) setPanOffset({ x: 0, y: 0 })
          return next
        })
      }
      if (e.key === "0") {
        setZoomScale(1)
        setPanOffset({ x: 0, y: 0 })
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [zoomedPageIdx, allSheets.length])

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
        reuse: 99.0 * factor,
        avail: 99.4 * factor,
      })

      if (progress < 1) {
        animationFrameId = requestAnimationFrame(tick)
      }
    }

    animationFrameId = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(animationFrameId)
  }, [isInView])

  // Key SLA / Target badges in the left column
  const targets = [
    {
      icon: <Droplet className="w-3.5 h-3.5 text-emerald-600 fill-emerald-600" />,
      label: "Sewage Treatment Target",
      value: "≥99%",
    },
    {
      icon: <Settings className="w-3.5 h-3.5 text-emerald-600 stroke-2" />,
      label: "STP Availability Target",
      value: "≥99.4%",
    },
    {
      icon: <Users className="w-3.5 h-3.5 text-emerald-600 stroke-2" />,
      label: "Manpower Coverage Target",
      value: "100%",
    },
  ]

  const activeZoomedSheet = zoomedPageIdx !== null ? allSheets[zoomedPageIdx] : null

  return (
    <section
      ref={sectionRef}
      id="performance"
      className="min-h-[calc(100vh-68px)] lg:h-[calc(100vh-68px)] flex flex-col justify-center w-full blueprint-grid relative overflow-hidden bg-gradient-to-b from-white via-sky-50/35 to-white text-slate-900 py-3 sm:py-4 px-3 sm:px-6 lg:px-8 border-t border-sky-100"
      style={{ ["--mx" as any]: "50%", ["--my" as any]: "50%" }}
    >
      {/* Decorative ambient curves */}
      <div className="absolute -bottom-16 -right-16 w-80 h-80 bg-sky-200/40 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" aria-hidden="true" />
      <div className="absolute -top-16 -left-16 w-72 h-72 bg-cyan-200/35 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" aria-hidden="true" />

      <div className="max-w-[1440px] mx-auto w-full relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 items-center">
        {/* ================= LEFT COLUMN: 100% PRESERVED CONTENT ================= */}
        <motion.div
          className="lg:col-span-5 xl:col-span-5 flex flex-col justify-between gap-2.5 sm:gap-3"
          initial={{ opacity: 0, x: -16 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Top Kicker */}
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-sky-50/90 border border-sky-200/80 w-fit shadow-2xs">
            <span className="w-3.5 h-0.5 bg-sky-500 rounded-full" />
            <span className="font-mono text-[9px] sm:text-[10px] font-bold text-sky-700 tracking-wider uppercase">
              STP OPERATIONS &amp; MAINTENANCE AUDIT
            </span>
          </div>

          {/* Headline */}
          <h2 className="font-display text-xl sm:text-2xl lg:text-[25px] xl:text-[28px] font-extrabold tracking-tight leading-[1.15]">
            <span className="text-[#0B2545] block">Performance You Can Measure.</span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 via-sky-500 to-cyan-600 block">
              Documented Every Single Month.
            </span>
          </h2>

          <p className="text-[11.5px] sm:text-xs text-slate-600 leading-relaxed font-normal">
            No vague verbal updates or missing logs. We deliver rigorous, data-driven monthly reports with Statistical Process Control (SPC), equipment uptime, and chemical stability metrics.
          </p>

          {/* 3 Compact Target Badges */}
          <div className="grid grid-cols-3 gap-1.5 pt-0.5">
            {targets.map((tgt, idx) => (
              <div
                key={idx}
                className="flex flex-col items-center justify-center text-center p-1.5 rounded-xl bg-white/90 border border-slate-200/80 shadow-2xs hover:border-sky-300 transition-all"
              >
                <div className="w-6 h-6 rounded-md bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-0.5">
                  {tgt.icon}
                </div>
                <span className="font-mono text-xs sm:text-sm font-extrabold text-[#0B2545] leading-none">
                  {tgt.value}
                </span>
                <span className="text-[8.5px] sm:text-[9px] text-slate-600 font-medium leading-tight mt-0.5">
                  {tgt.label}
                </span>
              </div>
            ))}
          </div>

          {/* Plant Photo with Verified Client Badge */}
          <div className="relative w-full h-[140px] sm:h-[155px] lg:h-[175px] xl:h-[190px] rounded-xl overflow-hidden border border-sky-200/90 bg-slate-100 shadow-sm group">
            <div ref={photoRef} className="absolute inset-[-2px] transition-transform duration-200 ease-out">
              <Image
                src="/images/crops/perf_plant.jpg"
                alt="STP Sewage Treatment Plant Operations"
                fill
                sizes="(max-width: 1024px) 100vw, 40vw"
                className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              />
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-black/55 via-black/10 to-transparent pointer-events-none" />
            
            <div className="absolute bottom-2 left-2 bg-white/95 backdrop-blur-md px-2 py-0.5 rounded-full border border-sky-200 shadow-sm flex items-center gap-1.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
              </span>
              <span className="text-[8.5px] font-mono font-bold text-slate-800 uppercase tracking-wider">
                Audited Client Site: Prestige Polygon
              </span>
            </div>
          </div>
        </motion.div>

        {/* ================= RIGHT COLUMN: COMBINED ACTUAL REPORT PAGES (MAX HEIGHT) ================= */}
        <motion.div
          className="lg:col-span-7 xl:col-span-7 flex flex-col"
          initial={{ opacity: 0, x: 16 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.5, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Main Card Container */}
          <div
            ref={reportRef}
            className="rounded-2xl border border-slate-200/90 shadow-xl bg-white overflow-hidden transition-transform duration-200 ease-out relative flex flex-col"
          >
            {/* Header: Title & 2-Module Segmented Selector */}
            <div className="bg-gradient-to-r from-sky-600 via-sky-700 to-sky-800 text-white px-3 sm:px-4 py-2 sm:py-2.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-sky-500/30 shadow-xs">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-white/10 border border-white/20 flex items-center justify-center text-sky-200 shadow-inner shrink-0">
                  <FileText className="w-3.5 h-3.5 text-white" />
                </div>
                <div>
                  <h3 className="font-display text-xs sm:text-sm font-bold text-white tracking-tight leading-snug">
                    Actual STP Performance Report
                  </h3>
                  <p className="text-[9.5px] text-sky-200/90 leading-tight">
                    Audited Engineering Telemetry &amp; Statistical Quality Records
                  </p>
                </div>
              </div>

              {/* Module Switcher Pills */}
              <div className="flex items-center bg-white/10 p-0.5 rounded-lg border border-white/20 self-start sm:self-auto shrink-0">
                <button
                  type="button"
                  onClick={() => setActiveModule("water")}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-[10px] sm:text-[11px] font-bold transition-all cursor-pointer ${
                    activeModule === "water"
                      ? "bg-white text-sky-800 shadow-xs"
                      : "text-white/80 hover:text-white"
                  }`}
                >
                  <BookOpen className="w-3 h-3 shrink-0" />
                  <span>Water Consumption</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveModule("tank")}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-[10px] sm:text-[11px] font-bold transition-all cursor-pointer ${
                    activeModule === "tank"
                      ? "bg-white text-sky-800 shadow-xs"
                      : "text-white/80 hover:text-white"
                  }`}
                >
                  <Layers className="w-3 h-3 shrink-0" />
                  <span>Tank Level Management</span>
                </button>
              </div>
            </div>

            {/* Document Canvas (Expansive Full Height) */}
            <div className="p-2 sm:p-2.5 lg:p-3 bg-slate-50/40">
              <AnimatePresence mode="wait">
                {activeModule === "water" ? (
                  /* MODULE 1: WATER CONSUMPTION SPREAD */
                  <motion.div
                    key="water-spread"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.25 }}
                    className="grid grid-cols-1 md:grid-cols-2 gap-2 sm:gap-2.5"
                  >
                    {/* Water SPC */}
                    <div
                      onClick={() => setZoomedPageIdx(0)}
                      className="group/p3 rounded-xl border border-slate-200 bg-white p-2 flex flex-col justify-between shadow-2xs hover:border-sky-300 hover:shadow-md transition-all cursor-pointer"
                    >
                      <div className="flex items-center justify-between pb-1.5 border-b border-slate-100 mb-1">
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-bold text-[#0B2545] truncate">
                            Water Consumption SPC
                          </span>
                        </div>
                        <span className="text-[8.5px] font-mono text-emerald-700 bg-emerald-50 px-1.5 py-0.2 rounded font-bold">
                          LIMIT CONTROL
                        </span>
                      </div>

                      {/* Viewport */}
                      <div className="relative w-full h-[260px] xs:h-[290px] sm:h-[320px] md:h-[350px] lg:h-[385px] xl:h-[415px] rounded-lg overflow-hidden bg-slate-50 border border-slate-200/90 shadow-2xs flex items-center justify-center group-hover/p3:border-sky-400 transition-colors">
                        <Image
                          src="/images/reports/water_consumption_spc_p3.png"
                          alt="Water Consumption SPC Charts"
                          fill
                          sizes="(max-width: 1024px) 100vw, 35vw"
                          className="object-contain p-1 select-none transition-transform duration-300 group-hover/p3:scale-[1.02]"
                          priority
                        />
                        <div className="absolute inset-0 bg-sky-950/20 backdrop-blur-[1px] opacity-0 group-hover/p3:opacity-100 transition-opacity duration-200 flex items-center justify-center z-10">
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white text-[#0B2545] font-bold text-[9px] shadow-md border border-sky-200">
                            <ZoomIn className="w-3 h-3 text-sky-600" />
                            <span>Click to Inspect</span>
                          </span>
                        </div>
                      </div>

                      <div className="pt-1 mt-1 border-t border-slate-100 text-[9px] text-slate-600 flex items-center justify-between">
                        <span>Filter Feed, SBR &amp; Flushing Lines</span>
                        <span className="font-mono text-sky-700 font-bold">UCL / LCL Bands</span>
                      </div>
                    </div>

                    {/* MBBR Process Stability */}
                    <div
                      onClick={() => setZoomedPageIdx(1)}
                      className="group/p11 rounded-xl border border-sky-300 ring-1 ring-sky-200/60 bg-gradient-to-b from-sky-50/20 to-white p-2 flex flex-col justify-between shadow-2xs hover:border-sky-400 hover:shadow-md transition-all cursor-pointer"
                    >
                      <div className="flex items-center justify-between pb-1.5 border-b border-slate-100 mb-1">
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-bold text-[#0B2545] truncate">
                            MBBR Process Stability
                          </span>
                        </div>
                        <span className="text-[8.5px] font-mono text-amber-700 bg-amber-50 px-1.5 py-0.2 rounded font-bold">
                          CV: 49.21%
                        </span>
                      </div>

                      {/* Viewport */}
                      <div className="relative w-full h-[260px] xs:h-[290px] sm:h-[320px] md:h-[350px] lg:h-[385px] xl:h-[415px] rounded-lg overflow-hidden bg-slate-50 border border-slate-200/90 shadow-2xs flex items-center justify-center group-hover/p11:border-sky-400 transition-colors">
                        <Image
                          src="/images/reports/water_consumption_stability_p11.png"
                          alt="MBBR Process Stability Analysis"
                          fill
                          sizes="(max-width: 1024px) 100vw, 35vw"
                          className="object-contain p-1 select-none transition-transform duration-300 group-hover/p11:scale-[1.02]"
                          priority
                        />
                        <div className="absolute inset-0 bg-sky-950/20 backdrop-blur-[1px] opacity-0 group-hover/p11:opacity-100 transition-opacity duration-200 flex items-center justify-center z-10">
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white text-[#0B2545] font-bold text-[9px] shadow-md border border-sky-200">
                            <ZoomIn className="w-3 h-3 text-sky-600" />
                            <span>Click to Inspect</span>
                          </span>
                        </div>
                      </div>

                      <div className="pt-1 mt-1 border-t border-slate-100 text-[9px] text-slate-600 flex items-center justify-between">
                        <span>Mean 77.60 KL • Std Dev 38.19 KL</span>
                        <span className="font-mono text-cyan-700 font-bold">Variability Zones</span>
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  /* MODULE 2: TANK LEVEL SPREAD */
                  <motion.div
                    key="tank-spread"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.25 }}
                    className="grid grid-cols-1 md:grid-cols-2 gap-2 sm:gap-2.5"
                  >
                    {/* Tank Level Control Charts */}
                    <div
                      onClick={() => setZoomedPageIdx(2)}
                      className="group/p2 rounded-xl border border-slate-200 bg-white p-2 flex flex-col justify-between shadow-2xs hover:border-sky-300 hover:shadow-md transition-all cursor-pointer"
                    >
                      <div className="flex items-center justify-between pb-1.5 border-b border-slate-100 mb-1">
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-bold text-[#0B2545] truncate">
                            Tank Level Control Charts
                          </span>
                        </div>
                        <span className="text-[8.5px] font-mono text-emerald-700 bg-emerald-50 px-1.5 py-0.2 rounded font-bold">
                          ZERO OVERFLOWS
                        </span>
                      </div>

                      <div className="relative w-full h-[260px] xs:h-[290px] sm:h-[320px] md:h-[350px] lg:h-[385px] xl:h-[415px] rounded-lg overflow-hidden bg-slate-50 border border-slate-200/90 shadow-2xs flex items-center justify-center group-hover/p2:border-sky-400 transition-colors">
                        <Image
                          src="/images/reports/tank_level_control_charts_p2.png"
                          alt="Tank Level Control Charts"
                          fill
                          sizes="(max-width: 1024px) 100vw, 35vw"
                          className="object-contain p-1 select-none transition-transform duration-300 group-hover/p2:scale-[1.02]"
                          priority
                        />
                        <div className="absolute inset-0 bg-sky-950/20 backdrop-blur-[1px] opacity-0 group-hover/p2:opacity-100 transition-opacity duration-200 flex items-center justify-center z-10">
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white text-[#0B2545] font-bold text-[9px] shadow-md border border-sky-200">
                            <ZoomIn className="w-3 h-3 text-sky-600" />
                            <span>Click to Inspect</span>
                          </span>
                        </div>
                      </div>

                      <div className="pt-1 mt-1 border-t border-slate-100 text-[9px] text-slate-600 flex items-center justify-between">
                        <span>Treated Water (100%), Collection, Soft</span>
                        <span className="font-mono text-blue-700 font-bold">31-Day Limits</span>
                      </div>
                    </div>

                    {/* Treated Water Tank Process Stability Analysis */}
                    <div
                      onClick={() => setZoomedPageIdx(3)}
                      className="group/p5 rounded-xl border border-sky-300 ring-1 ring-sky-200/60 bg-gradient-to-b from-sky-50/20 to-white p-2 flex flex-col justify-between shadow-2xs hover:border-sky-400 hover:shadow-md transition-all cursor-pointer"
                    >
                      <div className="flex items-center justify-between pb-1.5 border-b border-slate-100 mb-1">
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-bold text-[#0B2545] truncate">
                            Treated Tank Process Stability
                          </span>
                        </div>
                        <span className="text-[8.5px] font-mono text-emerald-700 bg-emerald-50 px-1.5 py-0.2 rounded font-bold">
                          CV: 29.04%
                        </span>
                      </div>

                      <div className="relative w-full h-[260px] xs:h-[290px] sm:h-[320px] md:h-[350px] lg:h-[385px] xl:h-[415px] rounded-lg overflow-hidden bg-slate-50 border border-slate-200/90 shadow-2xs flex items-center justify-center group-hover/p5:border-sky-400 transition-colors">
                        <Image
                          src="/images/reports/tank_level_stability_p5.png"
                          alt="Treated Water Tank Stability Analysis"
                          fill
                          sizes="(max-width: 1024px) 100vw, 35vw"
                          className="object-contain p-1 select-none transition-transform duration-300 group-hover/p5:scale-[1.02]"
                          priority
                        />
                        <div className="absolute inset-0 bg-sky-950/20 backdrop-blur-[1px] opacity-0 group-hover/p5:opacity-100 transition-opacity duration-200 flex items-center justify-center z-10">
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white text-[#0B2545] font-bold text-[9px] shadow-md border border-sky-200">
                            <ZoomIn className="w-3 h-3 text-sky-600" />
                            <span>Click to Inspect</span>
                          </span>
                        </div>
                      </div>

                      <div className="pt-1 mt-1 border-t border-slate-100 text-[9px] text-slate-600 flex items-center justify-between">
                        <span>Mean Level 64.29% • Std Dev 18.67%</span>
                        <span className="font-mono text-emerald-700 font-bold">96.8% Safe Band</span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Bottom Unified CTA Bar */}
            <div className="px-3 sm:px-4 py-2.5 bg-white border-t border-slate-100 flex items-center justify-end">
              <button
                ref={ctaRef}
                type="button"
                onClick={onOpenReportModal}
                className="w-full sm:w-auto px-5 py-2 rounded-full bg-gradient-to-r from-sky-600 to-sky-700 hover:from-sky-700 hover:to-sky-800 text-white font-display font-bold text-[11px] sm:text-xs flex items-center justify-center gap-1.5 transition-all duration-200 shadow-sm shadow-sky-600/25 hover:shadow-sky-600/40 relative overflow-hidden group cursor-pointer"
              >
                <span>Request Sample Report</span>
                <ArrowRight className="w-3.5 h-3.5 stroke-[2.5] transition-transform duration-300 group-hover:translate-x-1" />
              </button>
            </div>
          </div>
        </motion.div>
      </div>

      {/* ================= FULL-RESOLUTION FIT-TO-SCREEN LIGHTBOX ZOOM MODAL ================= */}
      <AnimatePresence>
        {activeZoomedSheet !== null && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 overflow-hidden select-none">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setZoomedPageIdx(null)}
              className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm"
            />

            {/* Modal Dialog */}
            <motion.div
              ref={modalRef}
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.96 }}
              transition={{ duration: 0.2 }}
              className="relative w-full max-w-5xl h-[92vh] max-h-[92vh] bg-white rounded-2xl shadow-2xl overflow-hidden z-10 flex flex-col border border-sky-100 overscroll-contain"
            >
              {/* Lightbox Header with Nanneer Sky/Blue Palette */}
              <div className="bg-gradient-to-r from-sky-600 via-sky-700 to-sky-800 text-white px-4 py-3 flex flex-col md:flex-row md:items-center justify-between gap-2.5 border-b border-sky-500/30 shrink-0">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-white/10 border border-white/20 flex items-center justify-center text-white shrink-0 mt-0.5">
                    <FileText className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-[9px] font-bold text-sky-200 bg-white/10 px-2 py-0.5 rounded border border-white/15 uppercase tracking-wider">
                        {activeZoomedSheet.docCategory}
                      </span>
                      <h4 className="font-display font-bold text-xs sm:text-sm text-white tracking-tight">
                        {activeZoomedSheet.title}
                      </h4>
                    </div>
                    {/* Clear "What this audit proves" context */}
                    <p className="text-[10.5px] sm:text-[11px] text-sky-100 font-medium leading-snug mt-1 flex items-start gap-1.5 max-w-2xl">
                      <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0 mt-1" />
                      <span>
                        <strong className="text-white font-bold">What this proves: </strong>
                        {activeZoomedSheet.finding}
                      </span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 sm:gap-2.5 self-end md:self-auto shrink-0">
                  {/* Interactive Zoom Level Controls */}
                  <div className="flex items-center bg-white/10 rounded-lg p-0.5 border border-white/20">
                    <button
                      type="button"
                      onClick={() => {
                        const newScale = Math.max(1, +(zoomScale - 0.4).toFixed(1))
                        setZoomScale(newScale)
                        if (newScale <= 1) setPanOffset({ x: 0, y: 0 })
                      }}
                      disabled={zoomScale <= 1}
                      className="p-1 hover:bg-white/20 disabled:opacity-40 rounded text-sky-100 hover:text-white transition cursor-pointer"
                      title="Zoom Out"
                    >
                      <ZoomOut className="w-3.5 h-3.5" />
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setZoomScale(1)
                        setPanOffset({ x: 0, y: 0 })
                      }}
                      className="text-[9.5px] font-mono px-1.5 text-white font-bold hover:bg-white/20 rounded py-0.5 transition"
                      title="Click to Reset to 100% Fit"
                    >
                      {Math.round(zoomScale * 100)}%
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setZoomScale((prev) => Math.min(2.5, +(prev + 0.4).toFixed(1)))
                      }}
                      disabled={zoomScale >= 2.5}
                      className="p-1 hover:bg-white/20 disabled:opacity-40 rounded text-sky-100 hover:text-white transition cursor-pointer"
                      title="Zoom In"
                    >
                      <ZoomIn className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Previous / Next Stepper */}
                  <div className="flex items-center bg-white/10 rounded-lg p-0.5 border border-white/20">
                    <button
                      type="button"
                      onClick={() =>
                        setZoomedPageIdx((prev) =>
                          prev !== null && prev > 0 ? prev - 1 : allSheets.length - 1
                        )
                      }
                      className="p-1 hover:bg-white/20 rounded text-sky-100 hover:text-white transition cursor-pointer"
                      title="Previous Page (Up / Left Arrow / Scroll Up)"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>
                    <span className="text-[10px] font-mono px-2 text-white font-bold">
                      {(zoomedPageIdx ?? 0) + 1} / {allSheets.length}
                    </span>
                    <button
                      type="button"
                      onClick={() =>
                        setZoomedPageIdx((prev) =>
                          prev !== null && prev < allSheets.length - 1 ? prev + 1 : 0
                        )
                      }
                      className="p-1 hover:bg-white/20 rounded text-sky-100 hover:text-white transition cursor-pointer"
                      title="Next Page (Down / Right Arrow / Scroll Down)"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>

                  <button
                    type="button"
                    onClick={() => setZoomedPageIdx(null)}
                    className="p-1.5 rounded-lg text-sky-100 hover:text-white hover:bg-white/15 transition cursor-pointer"
                    title="Close (Esc)"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Fit-to-Screen Image Canvas with Interactive Pan & Zoom */}
              <div
                className={`relative flex-1 bg-slate-100/90 flex items-center justify-center p-2 sm:p-3 overflow-hidden select-none ${
                  zoomScale > 1 ? "cursor-grab active:cursor-grabbing" : "cursor-zoom-in"
                }`}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                onDoubleClick={toggleZoom}
              >
                {/* Floating Previous Arrow */}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation()
                    setZoomedPageIdx((prev) =>
                      prev !== null && prev > 0 ? prev - 1 : allSheets.length - 1
                    )
                  }}
                  className="absolute left-3 sm:left-6 z-20 w-10 h-10 rounded-full bg-white/95 hover:bg-sky-600 text-slate-700 hover:text-white border border-slate-200/90 flex items-center justify-center shadow-lg transition-all hover:scale-110 cursor-pointer"
                  title="Previous Page"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>

                {/* Animated Fit-to-Height A4 Document Sheet with Zero Animation Conflict */}
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeZoomedSheet.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="relative h-full max-h-[calc(90vh-105px)] aspect-[1654/2339] mx-auto flex items-center justify-center select-none"
                  >
                    <div
                      onClick={toggleZoom}
                      className="relative w-full h-full bg-white shadow-2xl rounded-lg overflow-hidden border border-slate-300 transition-transform duration-150 ease-out"
                      style={{
                        transform: `translate(${panOffset.x}px, ${panOffset.y}px) scale(${zoomScale})`,
                        transformOrigin: "center center",
                        cursor: zoomScale > 1 ? "grab" : "zoom-in",
                      }}
                    >
                      <Image
                        src={activeZoomedSheet.image}
                        alt={activeZoomedSheet.title}
                        fill
                        className="object-contain pointer-events-none"
                        priority
                      />
                    </div>
                  </motion.div>
                </AnimatePresence>

                {/* Floating Next Arrow */}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation()
                    setZoomedPageIdx((prev) =>
                      prev !== null && prev < allSheets.length - 1 ? prev + 1 : 0
                    )
                  }}
                  className="absolute right-3 sm:right-6 z-20 w-10 h-10 rounded-full bg-white/95 hover:bg-sky-600 text-slate-700 hover:text-white border border-slate-200/90 flex items-center justify-center shadow-lg transition-all hover:scale-110 cursor-pointer"
                  title="Next Page"
                >
                  <ChevronRight className="w-5 h-5" />
                </button>

                {/* Floating Helper Pill */}
                <div className="absolute bottom-2.5 z-20 pointer-events-none bg-slate-900/80 backdrop-blur-md text-white text-[9.5px] font-mono px-3.5 py-1 rounded-full border border-white/20 shadow-lg flex items-center gap-1.5">
                  {zoomScale > 1 ? (
                    <span>Click or double-click to reset (100%) • Drag to pan</span>
                  ) : (
                    <span>Click image to zoom in (180%) • Use + / − for custom zoom</span>
                  )}
                </div>
              </div>

              {/* Lightbox Footer Bar with Request Button Only */}
              <div className="bg-white border-t border-slate-200 px-4 py-2.5 flex items-center justify-end shrink-0">
                <button
                  type="button"
                  onClick={() => {
                    setZoomedPageIdx(null)
                    onOpenReportModal?.()
                  }}
                  className="px-5 py-2 rounded-full bg-gradient-to-r from-sky-600 to-sky-700 hover:from-sky-700 hover:to-sky-800 text-white font-display font-bold text-xs flex items-center gap-1.5 transition-all duration-200 shadow-sm shadow-sky-600/25 hover:shadow-sky-600/40 cursor-pointer"
                >
                  <span>Request Sample Report</span>
                  <ArrowRight className="w-3.5 h-3.5 stroke-[2.5]" />
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </section>
  )
}
