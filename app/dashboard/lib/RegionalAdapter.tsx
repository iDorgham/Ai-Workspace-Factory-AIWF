"use client"
import * as React from "react"

type Region = "GLOBAL" | "MENA" | "EGYPT"

interface RegionalContextType {
  region: Region
  setRegion: (r: Region) => void
  isRTL: boolean
}

const RegionalContext = React.createContext<RegionalContextType | undefined>(undefined)

export function RegionalAdapterProvider({ children }: { children: React.ReactNode }) {
  const [region, setRegion] = React.useState<Region>("MENA")
  
  const isRTL = region === "MENA" || region === "EGYPT"

  React.useEffect(() => {
    // Sync HTML dir attribute with regional RTL state
    document.documentElement.dir = isRTL ? "rtl" : "ltr"
    document.documentElement.lang = isRTL ? "ar" : "en"
  }, [isRTL])

  return (
    <RegionalContext.Provider value={{ region, setRegion, isRTL }}>
      <div className={isRTL ? "font-cairo" : "font-inter"}>
        {children}
      </div>
    </RegionalContext.Provider>
  )
}

export function useRegional() {
  const context = React.useContext(RegionalContext)
  if (context === undefined) {
    throw new Error("useRegional must be used within a RegionalAdapterProvider")
  }
  return context
}
