"use client"

import React from "react"
import { motion } from "framer-motion"
import { StpProcessSimulation } from "@/components/StpProcessSimulation"
import {
  ArrowRight,
  BarChart2,
  Droplet,
  AlertTriangle,
  ClipboardList,
  Users,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react"

interface HeroSectionProps {
  onOpenReportModal?: () => void
}

export function HeroSection({ onOpenReportModal }: HeroSectionProps) {
  const problems = [
    {
      title: "Water Wastage",
      desc: "Treated water not fully utilized.",
      icon: Droplet,
      accent: "text-sky-600 bg-sky-50 border-sky-200/80",
    },
    {
      title: "Unexpected Incidents",
      desc: "Overflows, breakdowns and complaints.",
      icon: AlertTriangle,
      accent: "text-amber-600 bg-amber-50 border-amber-200/80",
    },
    {
      title: "Poor Documentation",
      desc: "Incomplete logs and missing records.",
      icon: ClipboardList,
      accent: "text-emerald-600 bg-emerald-50 border-emerald-200/80",
    },
    {
      title: "Manpower Dependency",
      desc: "Constant supervision and follow-ups.",
      icon: Users,
      accent: "text-indigo-600 bg-indigo-50 border-indigo-200/80",
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.08,
        delayChildren: 0.04,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 14 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const },
    },
  }

  return (
    <section
      id="why-nanneer"
      className="min-h-[calc(100vh-68px)] lg:h-[calc(100vh-68px)] flex flex-col justify-between py-3.5 sm:py-4 lg:py-5 px-3 sm:px-8 max-w-[1440px] mx-auto w-full blueprint-grid relative overflow-hidden bg-gradient-to-b from-white via-sky-50/40 to-white"
    >
      {/* Decorative ambient soft wave background curve matching reference */}
      <div className="absolute -bottom-12 -left-12 w-80 h-80 bg-sky-200/60 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" />
      <div className="absolute -top-12 -right-12 w-72 h-72 bg-cyan-200/50 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" />

      {/* 1. Hero Upper Row: Copy & Actions (Left) + Plant Photo (Right) */}
      <motion.div
        className="grid grid-cols-1 lg:grid-cols-12 gap-5 lg:gap-8 items-center relative z-10"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Left Column */}
        <div className="lg:col-span-6 xl:col-span-5 space-y-3.5 sm:space-y-4 lg:space-y-4.5 xl:space-y-5">
          {/* Overline badge */}
          <motion.div variants={itemVariants} className="flex items-center">
            <span className="text-[9.5px] sm:text-[11px] font-mono font-bold uppercase tracking-wider text-sky-700 bg-sky-50/90 border border-sky-200/80 px-2.5 py-0.5 rounded-full shadow-2xs">
              STP OPERATIONS &amp; MAINTENANCE FOR COMMERCIAL BUILDINGS
            </span>
          </motion.div>

          {/* Main Headline */}
          <motion.h1
            variants={itemVariants}
            className="font-display text-[22px] sm:text-3xl lg:text-[2.55rem] xl:text-[2.95rem] font-black text-[#0B2545] tracking-tight leading-[1.1]"
          >
            Your STP Is Running.
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 via-sky-500 to-cyan-600">
              But Is It Delivering?
            </span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            variants={itemVariants}
            className="text-xs sm:text-sm lg:text-[14px] xl:text-[15px] text-slate-600 leading-relaxed max-w-xl font-normal"
          >
            We manage your STP 24×7 to maximize sewage treatment, recover reusable water,
            prevent operational failures, and keep every activity documented.
          </motion.p>

          {/* Bold callout */}
          <motion.div
            variants={itemVariants}
            className="inline-flex items-center gap-2 px-3 sm:px-3.5 py-1.5 rounded-xl bg-white/90 border border-sky-200 shadow-2xs text-[11px] sm:text-sm font-bold text-[#0B2545]"
          >
            <div className="w-4 h-4 rounded-md bg-sky-100 flex items-center justify-center text-sky-600 shrink-0">
              <ShieldCheck className="w-3 h-3" />
            </div>
            <span>Not just manpower. Complete operational accountability.</span>
          </motion.div>

          {/* Desktop Action Buttons (Inside Left Column) */}
          <motion.div variants={itemVariants} className="hidden lg:flex items-center gap-3 pt-1.5 lg:pt-2.5">
            <a
              href="#contact"
              className="inline-flex items-center justify-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 rounded-full bg-gradient-to-r from-sky-600 to-sky-700 hover:from-sky-700 hover:to-sky-800 text-white font-black text-xs sm:text-sm tracking-wide transition-all duration-200 shadow-md shadow-sky-600/25 hover:shadow-sky-600/40 hover:-translate-y-0.5 active:translate-y-0 group"
            >
              <span>Discuss Your STP</span>
              <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
            </a>

            <button
              type="button"
              onClick={onOpenReportModal}
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 sm:py-3 rounded-full bg-white hover:bg-sky-50 text-slate-800 font-bold text-xs sm:text-sm border border-slate-300 hover:border-sky-400 transition-all duration-200 shadow-xs hover:shadow hover:-translate-y-0.5 active:translate-y-0"
            >
              <BarChart2 className="w-4 h-4 text-sky-600" />
              <span>See Sample Report</span>
            </button>
          </motion.div>
        </div>

        {/* Right Column: Interactive Animated STP Simulation (Process Flow Digital Twin) */}
        <motion.div variants={itemVariants} className="lg:col-span-6 xl:col-span-7 flex flex-col justify-end items-center w-full">
          <StpProcessSimulation />

          {/* Mobile Action Buttons (Displayed immediately below simulation on mobile only) */}
          <div className="flex lg:hidden flex-col sm:flex-row items-stretch sm:items-center gap-2.5 sm:gap-3 pt-3 w-full">
            <a
              href="#contact"
              className="inline-flex items-center justify-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 rounded-full bg-gradient-to-r from-sky-600 to-sky-700 hover:from-sky-700 hover:to-sky-800 text-white font-black text-xs sm:text-sm tracking-wide transition-all duration-200 shadow-md shadow-sky-600/25 hover:shadow-sky-600/40 hover:-translate-y-0.5 active:translate-y-0 group"
            >
              <span>Discuss Your STP</span>
              <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
            </a>

            <button
              type="button"
              onClick={onOpenReportModal}
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 sm:py-3 rounded-full bg-white hover:bg-sky-50 text-slate-800 font-bold text-xs sm:text-sm border border-slate-300 hover:border-sky-400 transition-all duration-200 shadow-xs hover:shadow hover:-translate-y-0.5 active:translate-y-0"
            >
              <BarChart2 className="w-4 h-4 text-sky-600" />
              <span>See Sample Report</span>
            </button>
          </div>
        </motion.div>
      </motion.div>

      {/* 2. Lower Row: Managing an STP Shouldn't Be a Daily Headache */}
      <motion.div
        className="pt-4 sm:pt-5 lg:pt-6 border-t border-sky-100/90 relative z-10 shrink-0 pb-1 sm:pb-2.5"
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className="text-center max-w-3xl mx-auto mb-3 sm:mb-3.5">
          <div className="w-8 h-[2px] bg-sky-500 mx-auto rounded-full mb-1.5 shadow-[0_0_8px_rgba(14,165,233,0.5)]" />
          <h2 className="font-display text-base sm:text-lg lg:text-[1.32rem] font-black text-[#0B2545] tracking-tight">
            Managing an STP Shouldn&apos;t Be a Daily Headache.
          </h2>
          <p className="mt-0.5 text-[11px] sm:text-xs text-slate-600 leading-normal max-w-xl mx-auto font-normal">
            You have enough responsibilities managing your building. Your STP should not
            require constant follow-ups, unexpected interventions, or last-minute
            preparation for inspections.
          </p>
        </div>

        {/* 4 Crisp Modern Diagnostic Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-3.5">
          {problems.map((item, idx) => {
            const Icon = item.icon
            return (
              <motion.div
                key={idx}
                whileHover={{ y: -2, transition: { duration: 0.2 } }}
                className="blueprint-card flex items-center gap-3.5 p-3.5 sm:p-4 rounded-xl bg-white border border-slate-200/90 shadow-2xs hover:border-sky-300 hover:shadow-xs transition-all group"
              >
                <div
                  className={`w-10 h-10 sm:w-11 sm:h-11 rounded-xl flex items-center justify-center shrink-0 border ${item.accent} transition-transform duration-300 group-hover:scale-105 shadow-2xs`}
                >
                  <Icon className="w-4 h-4 sm:w-5 sm:h-5 stroke-[1.8]" />
                </div>
                <div>
                  <h3 className="text-xs sm:text-[12.5px] font-bold text-[#0B2545] group-hover:text-sky-700 transition-colors">
                    {item.title}
                  </h3>
                  <p className="text-[11px] text-slate-600 leading-tight mt-0.5 font-normal">
                    {item.desc}
                  </p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </section>
  )
}
