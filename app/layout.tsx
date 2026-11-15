import type { Metadata, Viewport } from "next"
import "./globals.css"

export const viewport: Viewport = {
  themeColor: "#0d9488",
  width: "device-width",
  initialScale: 1,
}

export const metadata: Metadata = {
  title: "Nanneer Global | STP Operations & Maintenance for Commercial Buildings",
  description:
    "Your STP is running. But is it delivering? Complete 24×7 STP operations, water recovery, and monthly performance reporting with absolute accountability.",
  icons: {
    icon: "/logo.png",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased selection:bg-teal-500 selection:text-white">
        {children}
      </body>
    </html>
  )
}

