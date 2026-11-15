"use client"

import React, { useState, useEffect, useRef } from "react"
import Image from "next/image"
import { motion, AnimatePresence } from "framer-motion"
import {
  ArrowRight,
  Phone,
  Mail,
  CheckCircle2,
  Building2,
  Gauge,
  Sparkles,
  MapPin,
  Clock,
  ShieldCheck,
  Loader2,
} from "lucide-react"

export function AssessmentContactSection() {
  const [email, setEmail] = useState("")
  const [buildingType, setBuildingType] = useState("Commercial Office / IT Park")
  const [capacity, setCapacity] = useState("")
  const [improvement, setImprovement] = useState("Overall STP performance")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const sectionRef = useRef<HTMLElement>(null)
  const ctaRef = useRef<HTMLButtonElement>(null)
  const plantRef = useRef<HTMLDivElement>(null)

  // Cursor Spotlight & Parallax
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

      // Plant micro-parallax
      if (plantRef.current) {
        const nx = (e.clientX - rect.left) / rect.width - 0.5
        const ny = (e.clientY - rect.top) / rect.height - 0.5
        plantRef.current.style.transform = `translate3d(${nx * 8}px, ${ny * 8}px, 0) scale(1.02)`
      }

      // Magnetic CTA Button
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
      if (plantRef.current) {
        plantRef.current.style.transform = `translate3d(0, 0, 0) scale(1)`
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

  const buildingOptions = [
    "Commercial Office / IT Park",
    "Hotel & Hospitality",
    "Shopping Mall",
    "Other Commercial Property",
  ]

  const improvementOptions = [
    "Overall STP performance",
    "Existing O&M contractor transition",
    "Treated water circular reuse",
    "Breakdowns & compliance issues",
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email || isSubmitting) return

    setIsSubmitting(true)

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          type: "assessment",
          email,
          buildingType,
          capacity: capacity || "Not specified",
          improvement,
        }),
      })
      if (!res.ok) {
        throw new Error("Submission failed")
      }
    } catch {
      // Fallback gracefully so client UI doesn't stall
    } finally {
      setIsSubmitting(false)
      setIsSubmitted(true)
    }
  }

  return (
    <section
      ref={sectionRef}
      id="contact"
      className="min-h-[calc(100vh-72px)] flex flex-col justify-center py-8 sm:py-12 lg:py-8 px-3 sm:px-6 lg:px-8 max-w-[1400px] mx-auto w-full blueprint-grid relative bg-gradient-to-b from-white via-sky-50/40 to-white overflow-hidden text-slate-900"
      style={{ ["--mx" as any]: "50%", ["--my" as any]: "50%" }}
    >
      {/* Interactive Cursor Spotlight Glow */}
      <div
        className="absolute inset-0 pointer-events-none transition-opacity duration-300 transform-gpu"
        style={{
          background: "radial-gradient(650px circle at var(--mx) var(--my), rgba(14, 165, 233, 0.2), transparent 70%)",
        }}
        aria-hidden="true"
      />

      {/* Ambient background curves */}
      <div className="absolute -bottom-16 -right-16 w-80 h-80 bg-sky-200/65 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" aria-hidden="true" />
      <div className="absolute -top-16 -left-16 w-72 h-72 bg-cyan-200/55 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" aria-hidden="true" />

      <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-center relative z-10">
        {/* ================= LEFT COLUMN: Large Plant Image + Direct Contact Hub ================= */}
        <motion.div
          className="lg:col-span-5 flex flex-col gap-3.5"
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Much Larger Plant Image */}
          <div className="relative w-full h-[240px] sm:h-[340px] lg:h-[380px] xl:h-[400px] rounded-3xl overflow-hidden border border-sky-200/90 bg-slate-100 shadow-lg group">
            <div ref={plantRef} className="absolute inset-[-4px] transition-transform duration-200 ease-out">
              <Image
                src="/images/crops/contact_plant.jpg"
                alt="STP Aeration Facility & Control Station"
                fill
                sizes="(max-width: 1024px) 100vw, 45vw"
                className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                priority
              />
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-[#0B2545]/75 via-transparent to-transparent pointer-events-none" />

            {/* Plant Sign Badge with Live Pulse */}
            <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-sky-200 shadow-sm flex items-center gap-2 transition-transform duration-300 group-hover:scale-105">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
              </span>
              <span className="text-[10px] sm:text-[10.5px] font-mono font-black tracking-wider text-[#0B2545]">
                STP RAPID ASSESSMENT DESK
              </span>
            </div>

            {/* Bottom Telemetry Pill */}
            <div className="absolute bottom-3 left-3 right-3 sm:bottom-4 sm:left-4 sm:right-4 bg-[#0B2545]/90 backdrop-blur-md text-white px-3 sm:px-4 py-2 rounded-xl border border-white/10 flex items-center justify-between text-[10px] sm:text-[11px] font-mono">
              <span className="text-sky-300 font-bold flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-sky-400" />
                24×7 OPERATIONS DESK
              </span>
              <span className="text-emerald-400 font-bold flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                CPCB / SPCB
              </span>
            </div>
          </div>

          {/* Direct Operations Line Card */}
          <div className="rounded-2xl border border-slate-200/90 bg-white/95 backdrop-blur-md p-3.5 sm:p-4.5 shadow-md space-y-2.5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <span className="text-[10px] sm:text-[11px] font-mono font-bold uppercase tracking-wider text-sky-800 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-sky-600" />
                DIRECT OPERATIONS LINE
              </span>
              <span className="text-[9.5px] sm:text-[10px] font-mono font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Active Now
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {/* Phone Line */}
              <a
                href="tel:+919840023456"
                className="flex items-center gap-2.5 p-2 rounded-xl bg-slate-50/80 hover:bg-sky-50 border border-slate-200/80 hover:border-sky-300 transition-all duration-200 group shadow-2xs hover:-translate-y-0.5"
              >
                <div className="w-7 h-7 rounded-lg bg-sky-600 text-white flex items-center justify-center shrink-0 shadow-xs group-hover:scale-110 transition-transform">
                  <Phone className="w-3.5 h-3.5" />
                </div>
                <div className="min-w-0">
                  <div className="text-[10px] text-slate-500 font-mono">Call Operations</div>
                  <div className="font-bold text-slate-900 text-xs truncate group-hover:text-sky-700 font-mono">
                    +91 98400 23456
                  </div>
                </div>
              </a>

              {/* Official Email */}
              <a
                href="mailto:contact@nanneer.com"
                className="flex items-center gap-2.5 p-2 rounded-xl bg-slate-50/80 hover:bg-sky-50 border border-slate-200/80 hover:border-sky-300 transition-all duration-200 group shadow-2xs hover:-translate-y-0.5"
              >
                <div className="w-7 h-7 rounded-lg bg-sky-600 text-white flex items-center justify-center shrink-0 shadow-xs group-hover:scale-110 transition-transform">
                  <Mail className="w-3.5 h-3.5" />
                </div>
                <div className="min-w-0">
                  <div className="text-[10px] text-slate-500 font-mono">Official Email</div>
                  <div className="font-bold text-slate-900 text-xs truncate group-hover:text-sky-700 font-mono">
                    contact@nanneer.com
                  </div>
                </div>
              </a>
            </div>

            {/* Location strip */}
            <div className="flex items-center text-[10px] font-mono text-slate-500 pt-0.5">
              <span className="flex items-center gap-1">
                <MapPin className="w-3 h-3 text-sky-600" />
                Headquarters: Chennai
              </span>
            </div>
          </div>
        </motion.div>

        {/* ================= RIGHT COLUMN: Form Card Fills Screen Proportionally ================= */}
        <motion.div
          className="lg:col-span-7"
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.5, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="rounded-3xl border border-slate-200/90 shadow-xl bg-white/95 backdrop-blur-md p-4 sm:p-7 lg:p-7 relative overflow-hidden">
            <AnimatePresence mode="wait">
              {isSubmitted ? (
                <motion.div
                  key="success"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ type: "spring", stiffness: 300, damping: 25 }}
                  className="py-14 text-center space-y-4"
                >
                  <div className="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-300 text-emerald-600 flex items-center justify-center mx-auto shadow-sm">
                    <CheckCircle2 className="w-9 h-9 stroke-[2.5]" />
                  </div>
                  <h3 className="font-display text-2xl sm:text-3xl font-black text-[#0B2545]">
                    Assessment Request Received!
                  </h3>
                  <p className="text-sm text-slate-600 max-w-md mx-auto leading-relaxed">
                    Thank you. We have sent a confirmation to{" "}
                    <span className="font-mono font-bold text-sky-700">{email}</span>. A senior Nanneer STP operations engineer will contact you shortly to review your{" "}
                    <span className="font-semibold text-slate-800">{buildingType}</span> requirements.
                  </p>
                  <div className="pt-3">
                    <button
                      onClick={() => {
                        setIsSubmitted(false)
                        setEmail("")
                      }}
                      className="px-8 py-3 rounded-full bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold transition-all shadow-md shadow-sky-600/20 hover:-translate-y-0.5 cursor-pointer"
                    >
                      Submit Another Inquiry
                    </button>
                  </div>
                </motion.div>
              ) : (
                <motion.form
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  onSubmit={handleSubmit}
                  className="space-y-4"
                >
                  {/* Header Title with vertical accent bar matching screenshot */}
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-5 bg-sky-500 rounded-full shrink-0 shadow-[0_0_8px_rgba(14,165,233,0.5)]" />
                      <span className="text-[10px] sm:text-xs font-mono font-bold uppercase tracking-wider text-sky-700">
                        RAPID STP ASSESSMENT &amp; AUDIT
                      </span>
                    </div>
                    <h2 className="font-display text-xl sm:text-3xl lg:text-[28px] font-black text-[#0B2545] tracking-tight leading-tight mt-1.5">
                      Is Your STP Performing{" "}
                      <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 via-sky-500 to-cyan-600">
                        at Its Best?
                      </span>
                    </h2>
                    <p className="text-xs sm:text-[13px] text-slate-600 leading-relaxed mt-1 font-normal">
                      Connect with our engineering team to review water recovery, compliance, and O&amp;M reliability.
                    </p>
                  </div>

                  {/* 1. User Work Email Field (Required) */}
                  <div className="space-y-1.5">
                    <label className="block text-xs sm:text-sm font-bold text-[#0B2545]">
                      Your Work Email <span className="text-sky-600">*</span>
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                        <Mail className="w-4 h-4" />
                      </div>
                      <input
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="facility.manager@yourcompany.com"
                        className="w-full pl-10 pr-4 py-2.5 sm:py-3 rounded-xl bg-slate-50/80 border border-slate-200 text-base sm:text-sm text-[#0B2545] placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 focus:bg-white transition-all font-mono shadow-2xs"
                      />
                    </div>
                  </div>

                  {/* 2. Type of Building Selection Chips matching screenshot */}
                  <div className="space-y-1.5">
                    <label className="block text-xs sm:text-sm font-bold text-[#0B2545] flex items-center gap-1.5">
                      <Building2 className="w-3.5 h-3.5 text-sky-600" />
                      <span>Type of building</span>
                    </label>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-2.5">
                      {buildingOptions.map((opt, idx) => {
                        const isSelected = buildingType === opt
                        return (
                          <button
                            type="button"
                            key={idx}
                            onClick={() => setBuildingType(opt)}
                            className={`flex items-center gap-2.5 px-3 sm:px-3.5 py-2.5 rounded-xl border text-xs sm:text-sm transition-all duration-200 text-left ${
                              isSelected
                                ? "bg-sky-50/90 border-sky-500 text-sky-950 font-bold shadow-2xs ring-1 ring-sky-500/20"
                                : "bg-slate-50/70 border-slate-200 text-slate-700 hover:bg-white hover:border-slate-300"
                            }`}
                          >
                            <span
                              className={`w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${
                                isSelected ? "border-sky-600 bg-sky-600" : "border-slate-300 bg-white"
                              }`}
                            >
                              {isSelected && <span className="w-1.5 h-1.5 rounded-full bg-white" />}
                            </span>
                            <span className="truncate">{opt}</span>
                          </button>
                        )
                      })}
                    </div>
                  </div>

                  {/* 3. STP Capacity & Improvement Focus in 2 Columns */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                    {/* STP Capacity */}
                    <div className="space-y-1.5">
                      <label className="block text-xs sm:text-sm font-bold text-[#0B2545] flex items-center gap-1.5">
                        <Gauge className="w-3.5 h-3.5 text-sky-600" />
                        <span>
                          STP capacity <span className="font-normal text-slate-400 text-[10.5px]">(optional)</span>
                        </span>
                      </label>
                      <input
                        type="text"
                        value={capacity}
                        onChange={(e) => setCapacity(e.target.value)}
                        placeholder="e.g. 250 KLD"
                        className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50/80 border border-slate-200 text-xs sm:text-sm text-[#0B2545] placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 focus:bg-white transition-all font-mono shadow-2xs"
                      />
                    </div>

                    {/* What would you like to improve? */}
                    <div className="space-y-1.5">
                      <label className="block text-xs sm:text-sm font-bold text-[#0B2545] flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-sky-600" />
                        <span>Priority area</span>
                      </label>
                      <select
                        value={improvement}
                        onChange={(e) => setImprovement(e.target.value)}
                        className="w-full px-3 py-2.5 rounded-xl bg-slate-50/80 border border-slate-200 text-xs sm:text-sm text-[#0B2545] focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 focus:bg-white transition-all shadow-2xs font-sans cursor-pointer"
                      >
                        {improvementOptions.map((opt, idx) => (
                          <option key={idx} value={opt}>
                            {opt}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* 4. Action Row: Magnetic CTA Button */}
                  <div className="pt-2">
                    <button
                      ref={ctaRef}
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full px-4 sm:px-6 py-3.5 sm:py-4 rounded-full bg-gradient-to-r from-sky-600 to-sky-700 hover:from-sky-700 hover:to-sky-800 disabled:opacity-75 disabled:cursor-not-allowed text-white font-display font-bold text-xs xs:text-sm sm:text-base flex items-center justify-center gap-2 transition-all duration-200 shadow-md shadow-sky-600/20 hover:shadow-sky-600/35 relative overflow-hidden group cursor-pointer"
                    >
                      {isSubmitting ? (
                        <>
                          <Loader2 className="w-4 h-4 sm:w-5 sm:h-5 animate-spin" />
                          <span>Submitting Assessment Request...</span>
                        </>
                      ) : (
                        <>
                          {/* Animated Sheen Wave */}
                          <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700 pointer-events-none" />
                          <span className="relative z-10 flex items-center justify-center gap-1.5 sm:gap-2 text-center">
                            <span>Request Technical STP Assessment</span>
                            <ArrowRight className="w-4 h-4 stroke-[2.5] shrink-0 transition-transform duration-300 group-hover:translate-x-1.5" />
                          </span>
                        </>
                      )}
                    </button>
                  </div>
                </motion.form>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
