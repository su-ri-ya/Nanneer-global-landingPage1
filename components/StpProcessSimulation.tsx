"use client"

import React from "react"
import { Wind, ShieldCheck } from "lucide-react"

export function StpProcessSimulation() {
  return (
    <div className="relative w-full rounded-2xl overflow-hidden border border-sky-200/90 bg-white/95 backdrop-blur-md shadow-xl shadow-sky-950/5 flex flex-col font-sans select-none">
      {/* 1. Sleek Minimalist Top Status Bar */}
      <div className="px-3 sm:px-3.5 py-1.5 bg-sky-50/50 border-b border-sky-100/80 flex items-center justify-between gap-2 z-20 flex-wrap">
        <div className="flex items-center gap-1.5 sm:gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
          </span>
          <span className="text-[9.5px] sm:text-[11px] font-mono font-bold tracking-wider uppercase text-slate-700">
            24×7 Pure Flow Process Simulation
          </span>
        </div>

        {/* Target Badge */}
        <div className="flex items-center gap-1 sm:gap-1.5 px-2 sm:px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-[9px] sm:text-[10px] font-mono font-bold shrink-0">
          <ShieldCheck className="w-3 h-3 text-emerald-600 shrink-0" />
          <span>≥99% Water Recovery</span>
          <span className="hidden sm:inline">&nbsp;&amp; Circular Reuse</span>
        </div>
      </div>

      {/* 2. Main Animated Canvas (Full Height, Pure Simulation) */}
      <div className="relative w-full h-[235px] sm:h-[265px] md:h-[285px] lg:h-[305px] xl:h-[320px] bg-gradient-to-b from-white via-sky-50/25 to-white overflow-hidden">
        {/* Delicate Blueprint Dot Grid */}
        <div
          className="absolute inset-0 pointer-events-none opacity-40"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, #0284c718 1px, transparent 0)`,
            backgroundSize: "20px 20px",
          }}
        />

        <svg
          viewBox="0 25 1000 425"
          className="w-full h-full object-contain"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            {/* Liquid Gradients for Light Theme */}
            <linearGradient id="lightAerationWater" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#BAE6FD" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#38BDF8" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.9" />
            </linearGradient>

            <linearGradient id="lightClarifierWater" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.9" />
              <stop offset="45%" stopColor="#7DD3FC" stopOpacity="0.85" />
              <stop offset="75%" stopColor="#0284C7" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#B45309" stopOpacity="0.9" />
            </linearGradient>

            <linearGradient id="lightDisinfectionWater" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#67E8F9" stopOpacity="0.85" />
            </linearGradient>

            <linearGradient id="vesselGlassGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#F0F9FF" stopOpacity="0.4" />
            </linearGradient>

            <linearGradient id="filterVesselGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0369A1" />
              <stop offset="50%" stopColor="#0284C7" />
              <stop offset="100%" stopColor="#075985" />
            </linearGradient>

            <linearGradient id="grassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#4ADE80" />
              <stop offset="100%" stopColor="#16A34A" />
            </linearGradient>

            {/* Soft Shadow */}
            <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="3" stdDeviation="4" floodColor="#0B2545" floodOpacity="0.08" />
            </filter>
          </defs>

          {/* ============================================================== */}
          {/* UPPER PIPELINES WITH ACTIVE FLUID FLOW */}
          {/* ============================================================== */}

          {/* 1. Influent Line */}
          <path d="M 20 170 L 100 170" stroke="#94A3B8" strokeWidth="6" strokeLinecap="round" fill="none" />
          <path d="M 20 170 L 100 170" stroke="#64748B" strokeWidth="3" strokeDasharray="5 7" fill="none">
            <animate attributeName="stroke-dashoffset" from="24" to="0" dur="0.9s" repeatCount="indefinite" />
          </path>

          {/* 2. Screening to Aeration */}
          <path d="M 180 170 L 250 170" stroke="#CBD5E1" strokeWidth="6" strokeLinecap="round" fill="none" />
          <path d="M 180 170 L 250 170" stroke="#0EA5E9" strokeWidth="3" strokeDasharray="5 7" fill="none">
            <animate attributeName="stroke-dashoffset" from="24" to="0" dur="0.8s" repeatCount="indefinite" />
          </path>

          {/* 3. Aeration to Clarifier */}
          <path d="M 370 160 L 440 160" stroke="#BAE6FD" strokeWidth="6" strokeLinecap="round" fill="none" />
          <path d="M 370 160 L 440 160" stroke="#0284C7" strokeWidth="3" strokeDasharray="5 7" fill="none">
            <animate attributeName="stroke-dashoffset" from="24" to="0" dur="0.8s" repeatCount="indefinite" />
          </path>

          {/* 4. Clarifier Overflow to Disinfection */}
          <path d="M 540 150 L 590 150" stroke="#A5F3FC" strokeWidth="5" strokeLinecap="round" fill="none" />
          <path d="M 540 150 L 590 150" stroke="#06B6D4" strokeWidth="2.5" strokeDasharray="4 6" fill="none">
            <animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.7s" repeatCount="indefinite" />
          </path>

          {/* 5. Disinfection to Tertiary Sand Filter */}
          <path d="M 660 150 L 710 150" stroke="#BAE6FD" strokeWidth="5" strokeLinecap="round" fill="none" />

          {/* Between Sand & Carbon Filter */}
          <path d="M 760 150 L 790 150" stroke="#BAE6FD" strokeWidth="5" strokeLinecap="round" fill="none" />

          {/* Carbon Filter to Recycled Water Distribution Manifold */}
          <path d="M 840 150 L 890 150 L 890 270" stroke="#6EE7B7" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <path d="M 840 150 L 890 150 L 890 270" stroke="#10B981" strokeWidth="3" strokeDasharray="5 6" strokeLinejoin="round" fill="none">
            <animate attributeName="stroke-dashoffset" from="22" to="0" dur="0.6s" repeatCount="indefinite" />
          </path>

          {/* Horizontal Distribution Header to the 3 Reuse Fixtures */}
          <path d="M 570 270 L 910 270" stroke="#6EE7B7" strokeWidth="5" strokeLinecap="round" fill="none" />
          <path d="M 910 270 L 570 270" stroke="#10B981" strokeWidth="2.5" strokeDasharray="4 6" fill="none">
            <animate attributeName="stroke-dashoffset" from="0" to="20" dur="0.8s" repeatCount="indefinite" />
          </path>

          {/* Feeder Pipe 1: Down to Gardening Sprinkler */}
          <path d="M 570 270 L 570 330" stroke="#6EE7B7" strokeWidth="4" strokeLinecap="round" fill="none" />
          <path d="M 570 270 L 570 330" stroke="#10B981" strokeWidth="2" strokeDasharray="3 4" fill="none">
            <animate attributeName="stroke-dashoffset" from="14" to="0" dur="0.5s" repeatCount="indefinite" />
          </path>

          {/* Feeder Pipe 2: Down to Toilet Flush */}
          <path d="M 720 270 L 720 325" stroke="#6EE7B7" strokeWidth="4" strokeLinecap="round" fill="none" />
          <path d="M 720 270 L 720 325" stroke="#10B981" strokeWidth="2" strokeDasharray="3 4" fill="none">
            <animate attributeName="stroke-dashoffset" from="14" to="0" dur="0.5s" repeatCount="indefinite" />
          </path>

          {/* Feeder Pipe 3: Down to Softener & Cooling Tower */}
          <path d="M 850 270 L 850 325" stroke="#6EE7B7" strokeWidth="4" strokeLinecap="round" fill="none" />
          <path d="M 850 270 L 850 325" stroke="#10B981" strokeWidth="2" strokeDasharray="3 4" fill="none">
            <animate attributeName="stroke-dashoffset" from="14" to="0" dur="0.5s" repeatCount="indefinite" />
          </path>

          {/* 6. Clarifier Bottom Sludge Line (Underflow to Dewatering) */}
          <path d="M 490 235 L 490 340 L 395 340" stroke="#FDE68A" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <path d="M 490 235 L 490 340 L 395 340" stroke="#D97706" strokeWidth="2.5" strokeDasharray="4 6" strokeLinejoin="round" fill="none">
            <animate attributeName="stroke-dashoffset" from="30" to="0" dur="1.2s" repeatCount="indefinite" />
          </path>

          {/* RAS Recirculation Loop */}
          <path d="M 490 270 L 260 270 L 260 230" stroke="#7DD3FC" strokeWidth="2" strokeDasharray="3 3" fill="none" />

          {/* ============================================================== */}
          {/* TANK 1: SCREENING & PRIMARY SEDIMENTATION */}
          {/* ============================================================== */}
          <g filter="url(#softShadow)">
            <rect x="100" y="105" width="80" height="110" rx="8" fill="#F8FAFC" stroke="#CBD5E1" strokeWidth="1.5" />
            <rect x="104" y="140" width="72" height="71" rx="4" fill="#E2E8F0" opacity="0.85" />
            <polygon points="104,211 176,211 160,190 120,190" fill="#CBD5E1" />
            <line x1="120" y1="115" x2="165" y2="190" stroke="#64748B" strokeWidth="2.5" strokeDasharray="2 3" />
            <text x="140" y="94" textAnchor="middle" fill="#475569" fontSize="9" fontWeight="bold" fontFamily="monospace">
              SCREENING
            </text>
          </g>

          {/* ============================================================== */}
          {/* TANK 2: AERATION BIOREACTOR */}
          {/* ============================================================== */}
          <g filter="url(#softShadow)">
            <rect x="250" y="70" width="120" height="160" rx="10" fill="url(#vesselGlassGrad)" stroke="#38BDF8" strokeWidth="2" />
            <rect x="254" y="100" width="112" height="126" rx="6" fill="url(#lightAerationWater)" />

            {/* Animated Fine-Bubble Aeration Diffusers */}
            <g>
              {[
                { cx: 270, cy: 190, r: 2.5, dur: "1.2s", d: "0s" },
                { cx: 285, cy: 210, r: 3.5, dur: "1.0s", d: "0.2s" },
                { cx: 300, cy: 175, r: 2.0, dur: "0.9s", d: "0.4s" },
                { cx: 315, cy: 200, r: 4.0, dur: "1.3s", d: "0.1s" },
                { cx: 330, cy: 180, r: 2.5, dur: "1.1s", d: "0.3s" },
                { cx: 345, cy: 205, r: 3.0, dur: "0.8s", d: "0.5s" },
              ].map((b, idx) => (
                <circle key={idx} cx={b.cx} cy={b.cy} r={b.r} fill="#FFFFFF" opacity="0.85">
                  <animate
                    attributeName="cy"
                    values={`${b.cy};${b.cy - 75};${b.cy - 85}`}
                    dur={b.dur}
                    begin={b.d}
                    repeatCount="indefinite"
                  />
                  <animate
                    attributeName="opacity"
                    values="0.3;0.95;0"
                    dur={b.dur}
                    begin={b.d}
                    repeatCount="indefinite"
                  />
                </circle>
              ))}
            </g>

            {/* Blower Pump Feed */}
            <path d="M 390 115 L 360 115 L 360 210 L 265 210" stroke="#0284C7" strokeWidth="2" fill="none" />
            <circle cx="395" cy="115" r="11" fill="#E0F2FE" stroke="#0284C7" strokeWidth="1.5" />
            <Wind x="388" y="108" className="w-3.5 h-3.5 text-sky-700" />

            <circle cx="280" cy="135" r="2" fill="#FFFFFF" opacity="0.8" />
            <circle cx="310" cy="150" r="2" fill="#FFFFFF" opacity="0.8" />
            <circle cx="340" cy="130" r="2" fill="#FFFFFF" opacity="0.8" />
            <circle cx="295" cy="165" r="2" fill="#FFFFFF" opacity="0.8" />

            <text x="310" y="58" textAnchor="middle" fill="#0284C7" fontSize="10" fontWeight="bold" fontFamily="monospace">
              AERATION BIOREACTOR
            </text>
          </g>

          {/* Microbe Lens Badge (Minimal) */}
          <g transform="translate(205, 235)">
            <circle cx="20" cy="20" r="18" fill="#F0F9FF" stroke="#38BDF8" strokeWidth="1.5" />
            <ellipse cx="16" cy="16" rx="5" ry="2.5" fill="#0EA5E9" transform="rotate(30 16 16)" />
            <ellipse cx="24" cy="22" rx="4" ry="2" fill="#10B981" transform="rotate(-20 24 22)" />
            <circle cx="12" cy="22" r="1.5" fill="#64748B" />
            <circle cx="26" cy="14" r="1.5" fill="#64748B" />
          </g>

          {/* ============================================================== */}
          {/* TANK 3: SECONDARY CLARIFIER / SETTLING HOPPER */}
          {/* ============================================================== */}
          <g filter="url(#softShadow)">
            <polygon
              points="440,105 540,105 540,175 490,235 440,175"
              fill="url(#lightClarifierWater)"
              stroke="#0284C7"
              strokeWidth="2"
            />
            <rect x="482" y="100" width="16" height="45" fill="#F8FAFC" stroke="#0284C7" strokeWidth="1" />
            <line x1="490" y1="145" x2="490" y2="220" stroke="#64748B" strokeWidth="1.5" />
            <line x1="465" y1="205" x2="515" y2="205" stroke="#94A3B8" strokeWidth="2" />

            <path d="M 440 115 L 444 120 L 448 115" stroke="#0284C7" strokeWidth="1.5" fill="none" />
            <path d="M 532 115 L 536 120 L 540 115" stroke="#0284C7" strokeWidth="1.5" fill="none" />

            <polygon points="465,208 515,208 490,235" fill="#92400E" opacity="0.9" />

            <text x="490" y="92" textAnchor="middle" fill="#0369A1" fontSize="9" fontWeight="bold" fontFamily="monospace">
              CLARIFIER
            </text>
          </g>

          {/* ============================================================== */}
          {/* TANK 4: SLUDGE DEWATERING & RECOVERY (BOTTOM-LEFT) */}
          {/* ============================================================== */}
          <g filter="url(#softShadow)">
            <rect x="175" y="315" width="220" height="95" rx="8" fill="#FFFBEB" stroke="#FDE68A" strokeWidth="1.5" />

            {/* Sludge Thickener */}
            <rect x="190" y="335" width="45" height="50" rx="4" fill="#FEF3C7" stroke="#D97706" strokeWidth="1.2" />
            <polygon points="190,375 235,375 212,390" fill="#B45309" />
            <text x="212" y="358" textAnchor="middle" fill="#92400E" fontSize="7.5" fontWeight="bold">
              Thickener
            </text>

            <line x1="235" y1="360" x2="260" y2="360" stroke="#D97706" strokeWidth="2.5" />

            {/* Drying Bed */}
            <rect x="260" y="340" width="50" height="42" rx="3" fill="#FDF6B2" stroke="#B45309" strokeWidth="1.2" />
            <line x1="260" y1="362" x2="310" y2="362" stroke="#D97706" strokeWidth="1" strokeDasharray="2 2" />
            <text x="285" y="357" textAnchor="middle" fill="#92400E" fontSize="7" fontWeight="bold">
              Drying Bed
            </text>

            <line x1="310" y1="360" x2="335" y2="360" stroke="#10B981" strokeWidth="2" />

            {/* Organic Compost Cake */}
            <polygon points="335,380 375,380 355,348" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.2" />
            <text x="355" y="372" textAnchor="middle" fill="#15803D" fontSize="7" fontWeight="bold">
              Fertilizer
            </text>

            <text x="185" y="328" fill="#B45309" fontSize="8" fontWeight="bold" fontFamily="monospace">
              SLUDGE TREATMENT
            </text>
          </g>

          {/* ============================================================== */}
          {/* TANK 5: CHLORINE DISINFECTION */}
          {/* ============================================================== */}
          <g filter="url(#softShadow)">
            <rect x="590" y="105" width="70" height="95" rx="6" fill="#F0FDFA" stroke="#2DD4BF" strokeWidth="1.5" />
            <rect x="593" y="125" width="64" height="71" rx="3" fill="url(#lightDisinfectionWater)" />
            <line x1="612" y1="125" x2="612" y2="175" stroke="#0D9488" strokeWidth="2" />
            <line x1="635" y1="145" x2="635" y2="195" stroke="#0D9488" strokeWidth="2" />
            <text x="625" y="94" textAnchor="middle" fill="#0F766E" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
              DISINFECTION
            </text>
          </g>

          {/* ============================================================== */}
          {/* TANK 6: TERTIARY DUAL MEDIA FILTERS (PSF & ACF) */}
          {/* ============================================================== */}
          <g filter="url(#softShadow)">
            {/* Pressure Sand Filter (PSF) */}
            <rect x="710" y="95" width="50" height="110" rx="10" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="1.5" />
            <rect x="714" y="135" width="42" height="40" fill="#FDE68A" opacity="0.8" />
            <text x="735" y="86" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              SAND
            </text>

            {/* Activated Carbon Filter (ACF) */}
            <rect x="790" y="95" width="50" height="110" rx="10" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="1.5" />
            <rect x="794" y="135" width="42" height="40" fill="#334155" opacity="0.85" />
            <text x="815" y="86" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              CARBON
            </text>

            <text x="775" y="222" textAnchor="middle" fill="#64748B" fontSize="7.5" fontFamily="monospace">
              POLISHING
            </text>
          </g>

          {/* ============================================================== */}
          {/* REUSE SIMULATION 1: CAMPUS GARDENING & IRRIGATION SPRINKLER */}
          {/* ============================================================== */}
          <g transform="translate(525, 305)" filter="url(#softShadow)">
            {/* Background Container Box */}
            <rect x="0" y="0" width="115" height="105" rx="8" fill="#F0FDF4" stroke="#BBF7D0" strokeWidth="1.2" />

            {/* Grass Turf Patch */}
            <path d="M 10 92 Q 57 84 105 92 L 105 100 L 10 100 Z" fill="url(#grassGrad)" />
            {/* Little Grass Blades */}
            <line x1="25" y1="88" x2="22" y2="80" stroke="#15803D" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="30" y1="87" x2="32" y2="78" stroke="#16A34A" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="80" y1="88" x2="77" y2="80" stroke="#15803D" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="86" y1="87" x2="88" y2="79" stroke="#16A34A" strokeWidth="1.5" strokeLinecap="round" />

            {/* Sprinkler Riser Post & Nozzle */}
            <line x1="57" y1="25" x2="57" y2="85" stroke="#0284C7" strokeWidth="3" strokeLinecap="round" />
            <rect x="52" y="58" width="10" height="7" rx="2" fill="#0369A1" />
            <circle cx="57" cy="58" r="4.5" fill="#F59E0B" />

            {/* Animated Sprinkler Water Droplets Arcing Over Lawn */}
            <g>
              {/* Left Spray Arc */}
              <circle cx="53" cy="56" r="2" fill="#38BDF8">
                <animate attributeName="cx" values="53;22;12" dur="0.9s" repeatCount="indefinite" />
                <animate attributeName="cy" values="56;68;86" dur="0.9s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="1;0.8;0" dur="0.9s" repeatCount="indefinite" />
              </circle>
              <circle cx="53" cy="56" r="1.5" fill="#0EA5E9">
                <animate attributeName="cx" values="53;30;20" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
                <animate attributeName="cy" values="56;72;88" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="1;0.7;0" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
              </circle>

              {/* Right Spray Arc */}
              <circle cx="61" cy="56" r="2" fill="#38BDF8">
                <animate attributeName="cx" values="61;88;100" dur="0.9s" repeatCount="indefinite" />
                <animate attributeName="cy" values="56;68;86" dur="0.9s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="1;0.8;0" dur="0.9s" repeatCount="indefinite" />
              </circle>
              <circle cx="61" cy="56" r="1.5" fill="#0EA5E9">
                <animate attributeName="cx" values="61;80;92" dur="0.8s" begin="0.25s" repeatCount="indefinite" />
                <animate attributeName="cy" values="56;70;88" dur="0.8s" begin="0.25s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="1;0.7;0" dur="0.8s" begin="0.25s" repeatCount="indefinite" />
              </circle>
            </g>

            {/* Clean Subtitle */}
            <text x="57" y="16" textAnchor="middle" fill="#166534" fontSize="8" fontWeight="bold" fontFamily="monospace">
              GARDENING
            </text>
            <text x="57" y="26" textAnchor="middle" fill="#15803D" fontSize="6.5">
              Automated Irrigation
            </text>
          </g>

          {/* ============================================================== */}
          {/* REUSE SIMULATION 2: DUAL-FLUSH TOILET SYSTEM */}
          {/* ============================================================== */}
          <g transform="translate(660, 305)" filter="url(#softShadow)">
            <rect x="0" y="0" width="105" height="105" rx="8" fill="#F0F9FF" stroke="#BAE6FD" strokeWidth="1.2" />

            {/* Ceramic Cistern (Upper Tank) */}
            <rect x="36" y="32" width="34" height="26" rx="4" fill="#FFFFFF" stroke="#0284C7" strokeWidth="1.5" />
            {/* Water Inside Cistern */}
            <rect x="38" y="42" width="30" height="14" rx="2" fill="#BAE6FD" opacity="0.85" />
            {/* Dual-Flush Chrome Button */}
            <rect x="50" y="28" width="7" height="4" rx="1" fill="#64748B" />

            {/* Downward Flush Conduit */}
            <line x1="53" y1="58" x2="53" y2="72" stroke="#38BDF8" strokeWidth="4" />
            {/* Animated Flush Water Stream Down Pipe */}
            <line x1="53" y1="58" x2="53" y2="72" stroke="#0284C7" strokeWidth="2" strokeDasharray="3 3">
              <animate attributeName="stroke-dashoffset" from="12" to="0" dur="0.4s" repeatCount="indefinite" />
            </line>

            {/* Ceramic Bowl */}
            <path d="M 33 72 C 33 94, 73 94, 73 72 Z" fill="#FFFFFF" stroke="#0284C7" strokeWidth="1.5" />
            {/* Water Pool in Bowl */}
            <ellipse cx="53" cy="80" rx="14" ry="5" fill="#38BDF8" opacity="0.8" />
            <ellipse cx="53" cy="80" rx="9" ry="2.5" fill="#0284C7" opacity="0.6">
              <animate attributeName="rx" values="7;11;7" dur="1.2s" repeatCount="indefinite" />
            </ellipse>

            {/* Clean Subtitle */}
            <text x="53" y="16" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              FLUSHING
            </text>
            <text x="53" y="26" textAnchor="middle" fill="#0284C7" fontSize="6.5">
              Dual-Plumbing Lines
            </text>
          </g>

          {/* ============================================================== */}
          {/* REUSE SIMULATION 3: WATER SOFTENER & HVAC COOLING TOWER */}
          {/* ============================================================== */}
          <g transform="translate(785, 305)" filter="url(#softShadow)">
            <rect x="0" y="0" width="195" height="105" rx="8" fill="#F0FDFA" stroke="#99F6E4" strokeWidth="1.2" />

            {/* --- UNIT A: WATER SOFTENER VESSEL --- */}
            <g transform="translate(15, 0)">
              {/* Softener Cylinder */}
              <rect x="0" y="32" width="32" height="60" rx="8" fill="#0C4A6E" stroke="#0284C7" strokeWidth="1.5" />
              {/* Multiport Valve on Top */}
              <rect x="10" y="25" width="12" height="8" rx="2" fill="#64748B" />
              {/* Amber Ion-Exchange Resin Bed */}
              <rect x="4" y="52" width="24" height="34" fill="#F59E0B" opacity="0.9" />
              {/* Resin Beads Dots */}
              <circle cx="10" cy="60" r="1.5" fill="#FEF3C7" />
              <circle cx="20" cy="65" r="1.5" fill="#FEF3C7" />
              <circle cx="15" cy="74" r="1.5" fill="#FEF3C7" />

              <text x="16" y="16" textAnchor="middle" fill="#0E7490" fontSize="7.5" fontWeight="bold" fontFamily="monospace">
                SOFTENER
              </text>
              <text x="16" y="24" textAnchor="middle" fill="#0284C7" fontSize="6">
                Ion Exchange
              </text>
            </g>

            {/* Connecting Pipe from Softener to Cooling Tower */}
            <line x1="47" y1="62" x2="80" y2="62" stroke="#10B981" strokeWidth="3" />
            <line x1="47" y1="62" x2="80" y2="62" stroke="#6EE7B7" strokeWidth="1.5" strokeDasharray="3 3">
              <animate attributeName="stroke-dashoffset" from="12" to="0" dur="0.4s" repeatCount="indefinite" />
            </line>

            {/* --- UNIT B: HVAC COOLING TOWER --- */}
            <g transform="translate(80, 0)">
              {/* Cooling Tower Body */}
              <rect x="0" y="36" width="95" height="56" rx="4" fill="#FFFFFF" stroke="#0D9488" strokeWidth="1.5" />

              {/* Air Intake Louvres on Sides */}
              <line x1="5" y1="60" x2="25" y2="60" stroke="#CBD5E1" strokeWidth="1.5" />
              <line x1="5" y1="68" x2="25" y2="68" stroke="#CBD5E1" strokeWidth="1.5" />
              <line x1="5" y1="76" x2="25" y2="76" stroke="#CBD5E1" strokeWidth="1.5" />
              <line x1="70" y1="60" x2="90" y2="60" stroke="#CBD5E1" strokeWidth="1.5" />
              <line x1="70" y1="68" x2="90" y2="68" stroke="#CBD5E1" strokeWidth="1.5" />
              <line x1="70" y1="76" x2="90" y2="76" stroke="#CBD5E1" strokeWidth="1.5" />

              {/* Water Spray Deck & Falling Mist */}
              <line x1="30" y1="48" x2="65" y2="48" stroke="#0284C7" strokeWidth="2" />
              {/* Animated Falling Mist Particles */}
              <g opacity="0.8">
                <circle cx="36" cy="52" r="1.5" fill="#38BDF8">
                  <animate attributeName="cy" values="52;82" dur="0.6s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="1;0" dur="0.6s" repeatCount="indefinite" />
                </circle>
                <circle cx="48" cy="52" r="1.5" fill="#38BDF8">
                  <animate attributeName="cy" values="52;82" dur="0.7s" begin="0.2s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="1;0" dur="0.7s" begin="0.2s" repeatCount="indefinite" />
                </circle>
                <circle cx="59" cy="52" r="1.5" fill="#38BDF8">
                  <animate attributeName="cy" values="52;82" dur="0.55s" begin="0.35s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="1;0" dur="0.55s" begin="0.35s" repeatCount="indefinite" />
                </circle>
              </g>

              {/* Top Fan Cowl & Animated Rotating Fan */}
              <rect x="35" y="24" width="25" height="13" rx="2" fill="#0F766E" stroke="#0D9488" strokeWidth="1" />
              {/* Rotating Fan Impeller Blades */}
              <g transform="translate(47.5, 30.5)">
                <circle cx="0" cy="0" r="2.5" fill="#FFFFFF" />
                <line x1="-7" y1="0" x2="7" y2="0" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round">
                  <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.5s" repeatCount="indefinite" />
                </line>
                <line x1="0" y1="-7" x2="0" y2="7" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round">
                  <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.5s" repeatCount="indefinite" />
                </line>
              </g>

              {/* Clean Subtitle */}
              <text x="47" y="16" textAnchor="middle" fill="#0F766E" fontSize="8" fontWeight="bold" fontFamily="monospace">
                HVAC COOLING
              </text>
              <text x="47" y="24" textAnchor="middle" fill="#0D9488" fontSize="6">
                Chilled Water Makeup
              </text>
            </g>
          </g>

          {/* Raw Sewage Intake Tag */}
          <g transform="translate(15, 145)">
            <rect x="0" y="0" width="75" height="30" rx="4" fill="#F1F5F9" stroke="#CBD5E1" strokeWidth="1" />
            <text x="37" y="14" textAnchor="middle" fill="#334155" fontSize="7.5" fontWeight="bold">
              INFLUENT
            </text>
            <text x="37" y="24" textAnchor="middle" fill="#64748B" fontSize="6.5">
              Raw Sewage
            </text>
          </g>
        </svg>
      </div>
    </div>
  )
}
