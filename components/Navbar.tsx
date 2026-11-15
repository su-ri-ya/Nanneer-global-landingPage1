"use client"

import React, { useState, useEffect } from "react"
import Link from "next/link"
import Image from "next/image"
import { ArrowRight, Menu, X } from "lucide-react"

const NAV_ITEMS = [
  { label: "Why Nanneer", href: "#why-nanneer", id: "why-nanneer" },
  { label: "Our Approach", href: "#our-approach", id: "our-approach" },
  { label: "Performance", href: "#performance", id: "performance" },
  { label: "Contact", href: "#contact", id: "contact" },
]

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const [activeSection, setActiveSection] = useState<string>("why-nanneer")

  const updateActiveSection = () => {
    const sectionIds = NAV_ITEMS.map((item) => item.id)
    const mainEl = document.querySelector("main")
    const isDesktopMainScroller =
      Boolean(mainEl && window.innerWidth >= 1024 && mainEl.scrollHeight > mainEl.clientHeight)

    const scrollY = isDesktopMainScroller && mainEl ? mainEl.scrollTop : window.scrollY
    setScrolled(scrollY > 20)

    // Check if user has reached bottom of the page
    let isBottom = false
    if (isDesktopMainScroller && mainEl) {
      isBottom = mainEl.scrollTop + mainEl.clientHeight >= mainEl.scrollHeight - 60
    } else {
      const docHeight = document.documentElement.scrollHeight
      isBottom = window.innerHeight + window.scrollY >= docHeight - 80
    }

    if (isBottom) {
      setActiveSection("contact")
      return
    }

    // Determine which section currently occupies the largest vertical slice of the viewport
    const navOffset = 70
    const viewportHeight = window.innerHeight
    let bestSection = sectionIds[0]
    let maxVisibleHeight = -1

    for (const id of sectionIds) {
      const el = document.getElementById(id)
      if (el) {
        const rect = el.getBoundingClientRect()
        const visibleTop = Math.max(rect.top, navOffset)
        const visibleBottom = Math.min(rect.bottom, viewportHeight)
        const visibleHeight = Math.max(0, visibleBottom - visibleTop)

        if (visibleHeight > maxVisibleHeight) {
          maxVisibleHeight = visibleHeight
          bestSection = id
        }
      }
    }

    if (maxVisibleHeight > 0) {
      setActiveSection(bestSection)
    }
  }

  useEffect(() => {
    let ticking = false
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateActiveSection()
          ticking = false
        })
        ticking = true
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true })
    updateActiveSection()

    return () => {
      window.removeEventListener("scroll", onScroll)
    }
  }, [])

  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = "hidden"
      // Immediately calculate the active section when drawer opens
      updateActiveSection()
    } else {
      document.body.style.overflow = ""
    }
    return () => {
      document.body.style.overflow = ""
    }
  }, [mobileMenuOpen])

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, targetId: string) => {
    e.preventDefault()
    setActiveSection(targetId)
    setMobileMenuOpen(false)

    // Ensure body scroll is unlocked before executing scrollIntoView
    setTimeout(() => {
      const targetElement = document.getElementById(targetId)
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth" })
        window.history.pushState(null, "", `#${targetId}`)
      }
    }, 20)
  }

  return (
    <>
      <header
        className={`sticky top-0 z-40 transition-all duration-300 ${
          scrolled
            ? "bg-white/95 backdrop-blur-md shadow-sm shadow-sky-900/5 border-b border-sky-100 py-2 sm:py-3"
            : "bg-white/90 backdrop-blur-xs border-b border-slate-100 py-2.5 sm:py-4"
        }`}
      >
        <div className="max-w-[1400px] mx-auto px-3 sm:px-8 flex items-center justify-between">
          {/* Left: Enriched & Enlarged Brand Logo */}
          <div className="flex-1 flex justify-start items-center">
            <Link href="/" className="flex items-center group" aria-label="Home">
              <div
                className="relative h-9 w-28 sm:h-12 sm:w-40 md:h-14 md:w-48 transition-transform duration-300 group-hover:scale-102"
                style={{ maxWidth: "192px", maxHeight: "56px" }}
              >
                <Image
                  src="/logo.png"
                  alt="Nanneer Global Logo"
                  fill
                  priority
                  sizes="(max-width: 640px) 112px, (max-width: 768px) 160px, 192px"
                  className="object-contain object-left"
                  style={{ maxWidth: "100%", maxHeight: "100%" }}
                />
              </div>
            </Link>
          </div>

          {/* Center: Centered Navigation Links with Active Highlighting */}
          <nav className="hidden md:flex items-center justify-center gap-6 lg:gap-8 text-[14px] lg:text-[15px] font-semibold">
            {NAV_ITEMS.map((item) => {
              const isActive = activeSection === item.id
              return (
                <a
                  key={item.id}
                  href={item.href}
                  onClick={(e) => handleNavClick(e, item.id)}
                  className={`relative py-1 transition-colors duration-200 ${
                    isActive
                      ? "text-sky-600 font-bold after:w-full"
                      : "text-slate-700 hover:text-sky-600 after:w-0 hover:after:w-full"
                  } after:absolute after:bottom-0 after:left-0 after:h-0.5 after:bg-sky-500 after:transition-all after:duration-300`}
                >
                  {item.label}
                </a>
              )
            })}
          </nav>

          {/* Right: CTA Button & Mobile Trigger */}
          <div className="flex-1 flex justify-end items-center gap-2 sm:gap-3">
            <a
              href="#contact"
              onClick={(e) => handleNavClick(e, "contact")}
              className="hidden sm:inline-flex items-center gap-2 px-5 sm:px-6 py-2.5 rounded-full bg-sky-600 hover:bg-sky-700 text-white font-bold text-xs sm:text-sm transition-all duration-200 shadow-md shadow-sky-600/20 hover:shadow-sky-600/35 hover:-translate-y-0.5 active:translate-y-0 group"
            >
              <span>Discuss Your STP</span>
              <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
            </a>

            {/* Mobile menu trigger */}
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="md:hidden p-2 rounded-xl text-slate-700 hover:text-sky-600 hover:bg-sky-50 transition"
              aria-label="Open navigation menu"
            >
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>
      </header>

      {/* Backdrop for Mobile Sidebar Drawer - Placed outside <header> for true full-screen overlay */}
      <div
        className={`fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-50 transition-opacity duration-300 md:hidden ${
          mobileMenuOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
        }`}
        onClick={() => setMobileMenuOpen(false)}
        aria-hidden="true"
      />

      {/* Mobile Slide-out Sidebar Drawer (Slides smoothly from Right, full screen height) */}
      <aside
        className={`fixed inset-y-0 right-0 h-dvh w-[280px] sm:w-[320px] max-w-[85vw] bg-white z-50 shadow-2xl flex flex-col justify-between transition-transform duration-300 ease-in-out md:hidden ${
          mobileMenuOpen ? "translate-x-0" : "translate-x-full"
        }`}
        aria-label="Mobile navigation"
      >
        {/* Drawer Header */}
        <div className="p-4 sm:p-5 border-b border-slate-100 flex items-center justify-between bg-white shrink-0">
          <div className="relative h-8 w-28 sm:h-9 sm:w-32">
            <Image
              src="/logo.png"
              alt="Nanneer Global Logo"
              fill
              className="object-contain object-left"
            />
          </div>
          <button
            type="button"
            onClick={() => setMobileMenuOpen(false)}
            className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition"
            aria-label="Close navigation menu"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Drawer Nav links with clear Active Section Highlighter */}
        <div className="flex-1 overflow-y-auto px-3 sm:px-4 py-5 space-y-2 bg-white">
          <div className="px-3 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Current Sections
          </div>
          {NAV_ITEMS.map((item) => {
            const isActive = activeSection === item.id
            return (
              <a
                key={item.id}
                href={item.href}
                onClick={(e) => handleNavClick(e, item.id)}
                className={`group flex items-center justify-between px-3.5 py-3 rounded-xl text-sm transition-all duration-200 ${
                  isActive
                    ? "bg-sky-50 text-sky-700 font-bold border-l-4 border-sky-600 shadow-xs"
                    : "text-slate-600 font-medium hover:text-sky-600 hover:bg-slate-50 border-l-4 border-transparent"
                }`}
              >
                <span>{item.label}</span>
                <ArrowRight
                  className={`w-4 h-4 transition-all duration-200 ${
                    isActive
                      ? "text-sky-600 opacity-100"
                      : "text-slate-300 opacity-0 group-hover:opacity-100"
                  }`}
                />
              </a>
            )
          })}
        </div>

        {/* Drawer Footer CTA */}
        <div className="p-4 sm:p-5 border-t border-slate-100 bg-slate-50 shrink-0 space-y-3">
          <a
            href="#contact"
            onClick={(e) => handleNavClick(e, "contact")}
            className="flex items-center justify-center gap-2 w-full py-3 px-4 rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-bold text-sm shadow-md shadow-sky-600/20 active:scale-[0.99] transition"
          >
            <span>Discuss Your STP</span>
            <ArrowRight className="w-4 h-4" />
          </a>
          <p className="text-center text-[10.5px] sm:text-[11px] text-slate-400">
            Zero Capex • Guaranteed Compliance
          </p>
        </div>
      </aside>
    </>
  )
}
