import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Integraty - AI Monitoring Platform',
  description: 'Professional monitoring system for examinations and assessments',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
