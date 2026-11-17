import type { Metadata, Viewport } from "next"
import "./globals.css"

export const viewport: Viewport = {
  themeColor: "#0284c7",
  width: "device-width",
  initialScale: 1,
}

export const metadata: Metadata = {
  metadataBase: new URL("https://nanneerconsultancy.com"),
  title: {
    default: "Nanneer Consultancy | Commercial STP Operations & Maintenance",
    template: "%s | Nanneer Consultancy",
  },
  description:
    "Nanneer Consultancy delivers complete 24×7 commercial STP operations, treated water recovery, MBBR biological management, tertiary filtration, and TNPCB compliance with monthly accountability.",
  keywords: [
    "Nanneer Consultancy",
    "STP operations and maintenance",
    "commercial sewage treatment plant",
    "STP plant operation Chennai",
    "STP maintenance Tamil Nadu",
    "MBBR sewage treatment plant",
    "sewage treatment plant AMC",
    "commercial water recycling",
    "tertiary filtration sand carbon",
    "STP water audit consultancy",
    "zero liquid discharge solutions",
    "TNPCB STP compliance",
    "SCADA STP monitoring",
    "commercial wastewater management",
    "STP operation contractor Chennai"
  ],
  authors: [{ name: "Nanneer Consultancy", url: "https://nanneerconsultancy.com" }],
  creator: "Nanneer Consultancy",
  publisher: "Nanneer Consultancy",
  alternates: {
    canonical: "https://nanneerconsultancy.com",
  },
  openGraph: {
    title: "Nanneer Consultancy | Commercial STP Operations & Maintenance",
    description:
      "Your STP is running. But is it delivering? 24×7 operations, water recovery, and monthly performance reporting with absolute accountability.",
    url: "https://nanneerconsultancy.com",
    siteName: "Nanneer Consultancy",
    locale: "en_IN",
    type: "website",
    images: [
      {
        url: "/nanneer_consultancy_logo.png",
        width: 1200,
        height: 630,
        alt: "Nanneer Consultancy - Commercial STP Operations",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Nanneer Consultancy | Commercial STP Operations & Maintenance",
    description:
      "Complete 24×7 STP operations, water recovery, and monthly performance reporting with absolute accountability.",
    images: ["/nanneer_consultancy_logo.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: [
      { url: "/favicon.ico" },
      { url: "/logo.png", type: "image/png" },
      { url: "/nanneer_consultancy_logo.png", type: "image/png" },
    ],
    apple: "/logo.png",
  },
  verification: {
    google: process.env.NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION || "",
  },
}

const organizationSchema = {
  "@context": "https://schema.org",
  "@type": ["Organization", "ProfessionalService"],
  name: "Nanneer Consultancy",
  url: "https://nanneerconsultancy.com",
  logo: "https://nanneerconsultancy.com/nanneer_consultancy_logo.png",
  image: "https://nanneerconsultancy.com/nanneer_consultancy_logo.png",
  description:
    "Premier environmental and sewage treatment plant (STP) operations & maintenance consultancy for commercial buildings, tech parks, hospitals, and residential townships across Tamil Nadu and India.",
  address: {
    "@type": "PostalAddress",
    addressLocality: "Chennai",
    addressRegion: "Tamil Nadu",
    addressCountry: "IN",
  },
  areaServed: [
    {
      "@type": "State",
      name: "Tamil Nadu",
    },
    {
      "@type": "Country",
      name: "India",
    },
  ],
  hasOfferCatalog: {
    "@type": "OfferCatalog",
    name: "STP Operation & Water Treatment Services",
    itemListElement: [
      {
        "@type": "Offer",
        itemOffered: {
          "@type": "Service",
          name: "24×7 Commercial STP Operations & Maintenance",
          description: "End-to-end operational management of MBBR, SBR, and ASP wastewater treatment plants.",
        },
      },
      {
        "@type": "Offer",
        itemOffered: {
          "@type": "Service",
          name: "Water Audit & Recovery Optimization",
          description: "Tertiary media filtration (PSF/ACF/Softener) calibration to maximize treated water reuse for flushing and landscaping.",
        },
      },
      {
        "@type": "Offer",
        itemOffered: {
          "@type": "Service",
          name: "Pollution Control Board (PCB) Compliance & Lab Testing",
          description: "Rigorous water quality testing, monthly parameter accountability, and statutory compliance reporting.",
        },
      },
    ],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
      </head>
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased selection:bg-teal-500 selection:text-white">
        {children}
      </body>
    </html>
  )
}

