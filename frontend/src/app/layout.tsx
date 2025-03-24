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
    <html lang="es" className="h-full">
      <body className={`${inter.className} h-full`}>
        <div className="flex flex-col h-full">
          <Header />
          <main className="flex-grow overflow-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}