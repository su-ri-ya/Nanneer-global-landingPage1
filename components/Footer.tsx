"use client"

import React from "react"
import Link from "next/link"
import Image from "next/image"
import { ShieldCheck, MapPin } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-slate-50/80 text-slate-600 pt-12 pb-8 border-t border-slate-200/90 lg:snap-start font-sans">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-8">
        {/* Main Footer Grid: Clean 3-Column Architectural Alignment */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-8 lg:gap-12 pb-10 border-b border-slate-200/80 items-start">
          {/* Column 1: Brand & Credibility (lg:col-span-6) */}
          <div className="lg:col-span-6 space-y-3.5">
            <Link href="/" className="inline-block" aria-label="Nanneer Consultancy Home">
              <div className="relative h-10 w-40 sm:h-11 sm:w-44">
                <Image
                  src="/logo.png"
                  alt="Nanneer Consultancy"
                  fill
                  className="object-contain object-left"
                />
              </div>
            </Link>

            <p className="text-xs sm:text-sm text-slate-600 max-w-md leading-relaxed font-normal">
              Complete Sewage Treatment Plant (STP) Operations &amp; Maintenance responsibility for Grade-A commercial buildings, IT parks, hospitality, and retail campuses.
            </p>

            <div className="pt-1 flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-mono font-bold shadow-2xs">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                100% CPCB &amp; SPCB Compliant
              </span>
            </div>
          </div>

          {/* Column 2: O&M Capabilities (lg:col-span-3) */}
          <div className="lg:col-span-3 space-y-3">
            <h4 className="text-[11px] font-mono font-bold text-sky-800 uppercase tracking-wider">
              O&amp;M Capabilities
            </h4>
            <ul className="space-y-2.5 text-xs font-medium text-slate-600">
              <li>
                <a href="#why-nanneer" className="hover:text-sky-600 transition-colors flex items-center gap-1.5">
                  <span className="text-sky-500 font-bold">›</span>
                  <span>24×7 3-Shift Plant Operations</span>
                </a>
              </li>
              <li>
                <a href="#our-approach" className="hover:text-sky-600 transition-colors flex items-center gap-1.5">
                  <span className="text-sky-500 font-bold">›</span>
                  <span>Circular Water Recovery (≥99%)</span>
                </a>
              </li>
              <li>
                <a href="#performance" className="hover:text-sky-600 transition-colors flex items-center gap-1.5">
                  <span className="text-sky-500 font-bold">›</span>
                  <span>Digital SCADA Telemetry &amp; Logs</span>
                </a>
              </li>
              <li>
                <a href="#contact" className="hover:text-sky-600 transition-colors flex items-center gap-1.5">
                  <span className="text-sky-500 font-bold">›</span>
                  <span>Preventive Equipment Maintenance</span>
                </a>
              </li>
            </ul>
          </div>

          {/* Column 3: Regional Presence (lg:col-span-3) */}
          <div className="lg:col-span-3 space-y-3">
            <h4 className="text-[11px] font-mono font-bold text-sky-800 uppercase tracking-wider">
              Headquarters
            </h4>
            <div className="space-y-2 text-xs">
              <div className="flex items-start gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-sky-50 border border-sky-200 text-sky-600 flex items-center justify-center shrink-0 mt-0.5">
                  <MapPin className="w-3.5 h-3.5" />
                </div>
                <div>
                  <div className="font-bold text-slate-800 text-sm">Chennai</div>
                  <div className="text-[11px] text-slate-500 font-mono mt-0.5">Commercial Tech Corridors</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar: Clean Copyright Notice */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-500">
          <div>
            &copy; {new Date().getFullYear()} Nanneer Consultancy. All rights reserved. Professional STP Operations &amp; Maintenance.
          </div>
        </div>
      </div>
    </footer>
  )
}
