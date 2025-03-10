import '@/styles/globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Header from '@/components/Header'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Smart Travel Planner',
  description: 'Asistente de viajes inteligente para la Universidad de Graz',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <div className="flex flex-col h-screen">
          <Header />
          <main className="flex-grow overflow-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}