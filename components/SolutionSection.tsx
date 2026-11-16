"use client"

import React from "react"
import Image from "next/image"
import { motion } from "framer-motion"
import { HardHat, Droplets, Laptop } from "lucide-react"

export function SolutionSection() {
  const solutions = [
    {
      title: "24×7 Plant Operations",
      description:
        "Trained operators across three shifts, supported by defined SOPs, supervision, and preventive maintenance.",
      icon: HardHat,
      image: "/images/crops/solution_op_indian.jpg",
      alt: "24x7 Plant Operations Operator",
      step: "01",
      badge: "3-Shift Coverage",
    },
    {
      title: "Maximum Water Recovery",
      description:
        "Measure, treat, and maximize safe reuse of wastewater for cooling towers, toilet flushing, and gardening.",
      icon: Droplets,
      image: "/images/crops/solution_water.jpg",
      alt: "Maximum Water Recovery Treated Water Weir",
      step: "02",
      badge: "≥99% Recovery",
    },
    {
      title: "Digital Monitoring & Accountability",
      description:
        "Track water quantity, quality, tank levels, equipment health, and scheduled activities with documented evidence.",
      icon: Laptop,
      image: "/images/crops/solution_digital_indian.jpg",
      alt: "Digital Monitoring and Accountability SCADA Screen",
      step: "03",
      badge: "Verified Logs",
    },
  ]

  return (
    <section
      id="our-approach"
      className="min-h-[calc(100vh-72px)] flex flex-col justify-center py-8 sm:py-12 lg:py-8 px-3 sm:px-8 max-w-[1400px] mx-auto w-full blueprint-grid relative overflow-hidden bg-gradient-to-b from-white via-sky-50/40 to-white"
    >
      {/* Ambient subtle light-blue background glows */}
      <div className="absolute -bottom-16 -right-16 w-80 h-80 bg-sky-200/60 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" />
      <div className="absolute -top-16 -left-16 w-72 h-72 bg-cyan-200/50 rounded-full blur-3xl pointer-events-none transform-gpu will-change-transform" />

      {/* Centered Heading */}
      <motion.div
        className="text-center max-w-3xl mx-auto mb-4 sm:mb-5 lg:mb-6 relative z-10"
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-50px" }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className="inline-flex items-center gap-2 mb-2 px-3 py-0.5 rounded-full bg-sky-50 border border-sky-200">
          <span className="w-2 h-2 rounded-full bg-sky-600 animate-pulse" />
          <span className="text-[10px] sm:text-xs font-mono font-bold uppercase tracking-wider text-sky-700">
            THE SOLUTION
          </span>
        </div>
        <h2 className="font-display text-xl sm:text-3xl lg:text-[2.35rem] font-black text-[#0B2545] tracking-tight">
          One Partner. Complete STP Responsibility.
        </h2>
        <p className="mt-1 text-xs sm:text-sm text-slate-600 leading-relaxed max-w-xl mx-auto font-normal">
          From operator deployment to water recovery and monthly reporting, we bring the
          essential elements of STP operations under one accountable service.
        </p>
      </motion.div>

      {/* Layout matching user reference: Featured top card + 2 bottom cards */}
      <div className="max-w-6xl mx-auto w-full relative z-10 flex flex-col gap-4 lg:gap-5">
        {/* Top Featured Card: 24×7 Plant Operations */}
        {(() => {
          const topItem = solutions[0]
          const TopIcon = topItem.icon

          return (
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
              className="relative flex flex-col md:flex-row rounded-3xl bg-white border border-slate-200/90 shadow-sm hover:border-sky-300 hover:shadow-md transition-all duration-300 overflow-hidden"
            >
              {/* Image side (~60%) */}
              <div className="relative w-full md:w-[58%] lg:w-[60%] min-h-[190px] sm:min-h-[260px] md:min-h-[270px] lg:min-h-[290px] overflow-hidden bg-slate-100">
                <Image
                  src={topItem.image}
                  alt={topItem.alt}
                  fill
                  sizes="(max-width: 768px) 100vw, 60vw"
                  className="object-cover"
                  priority
                />

                {/* Badges on Image */}
                <div className="absolute top-3.5 left-3.5 px-3 py-1 rounded-full bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-xs text-[10px] sm:text-[11px] font-mono font-bold text-slate-800 flex items-center gap-1.5 z-10">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  <span>MODULE // {topItem.step}</span>
                </div>

                <div className="absolute top-3.5 right-3.5 px-3 py-1 rounded-full bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-xs text-[10px] sm:text-[11px] font-mono font-bold text-sky-700 z-10">
                  {topItem.badge}
                </div>
              </div>

              {/* Content side (~40%) */}
              <div className="w-full md:w-[42%] lg:w-[40%] p-4 sm:p-7 lg:p-8 flex flex-col justify-center bg-white">
                <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-sky-50 text-sky-600 border border-sky-100 flex items-center justify-center shrink-0 shadow-2xs mb-2.5 sm:mb-4">
                  <TopIcon className="w-4 h-4 sm:w-5 sm:h-5 stroke-[2]" />
                </div>
                <h3 className="font-display text-xl sm:text-3xl lg:text-[2rem] font-extrabold text-[#0B2545] tracking-tight leading-tight">
                  {topItem.title}
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed mt-2 max-w-md font-normal">
                  {topItem.description}
                </p>
              </div>
            </motion.div>
          )
        })()}

        {/* Bottom Row: 2 Split Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-5">
          {solutions.slice(1).map((item, idx) => {
            const Icon = item.icon

            return (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 0.5, delay: (idx + 1) * 0.1, ease: [0.22, 1, 0.36, 1] }}
                className="relative flex flex-col sm:flex-row rounded-3xl bg-white border border-slate-200/90 shadow-sm hover:border-sky-300 hover:shadow-md transition-all duration-300 overflow-hidden"
              >
                {/* Image side (~48%) */}
                <div className="relative w-full sm:w-[48%] min-h-[180px] sm:min-h-[190px] lg:min-h-[210px] overflow-hidden bg-slate-100">
                  <Image
                    src={item.image}
                    alt={item.alt}
                    fill
                    sizes="(max-width: 768px) 100vw, 30vw"
                    className="object-cover"
                  />

                  {/* Badges on Image */}
                  <div className="absolute top-3 left-3 px-2.5 py-1 rounded-full bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-xs text-[10px] font-mono font-bold text-slate-800 flex items-center gap-1.5 z-10">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    <span>MODULE // {item.step}</span>
                  </div>

                  <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-xs text-[10px] font-mono font-bold text-sky-700 z-10">
                    {item.badge}
                  </div>
                </div>

                {/* Content side (~52%) */}
                <div className="w-full sm:w-[52%] p-5 sm:p-5 lg:p-6 flex flex-col justify-center bg-white">
                  <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-sky-50 text-sky-600 border border-sky-100 flex items-center justify-center shrink-0 shadow-2xs mb-2.5 sm:mb-3">
                    <Icon className="w-4 h-4 stroke-[2]" />
                  </div>
                  <h3 className="font-display text-base sm:text-lg lg:text-xl font-bold text-[#0B2545] tracking-tight leading-snug">
                    {item.title}
                  </h3>
                  <p className="text-[11px] sm:text-xs text-slate-600 leading-relaxed mt-1.5 font-normal">
                    {item.description}
                  </p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
