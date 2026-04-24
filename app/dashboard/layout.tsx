import * as React from "react"
import { Sidebar } from "./components/Sidebar"
import { Header } from "./components/Header"
import { PersistentChat } from "./components/PersistentChat"
import { RegionalAdapterProvider } from "./lib/RegionalAdapter"

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <RegionalAdapterProvider>
      <div className="flex h-screen overflow-hidden bg-background">
        {/* Collapsible Sidebar */}
        <Sidebar />

        <div className="flex flex-col flex-1 overflow-hidden">
          {/* Fixed Header */}
          <Header />

          {/* Main Content Area */}
          <main className="flex-1 overflow-y-auto p-space-4 scrollbar-industrial">
            <div className="container mx-auto">
              {children}
            </div>
          </main>
        </div>

        {/* Persistent AIChat Drawer/Sidebar */}
        <PersistentChat />
      </div>
    </RegionalAdapterProvider>
  )
}
