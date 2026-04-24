"use client"
import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { LayoutDashboard, Settings, MessageSquare, ChevronLeft, ChevronRight, Library } from "lucide-react"

export function Sidebar() {
  const [isCollapsed, setIsCollapsed] = React.useState(false)

  return (
    <aside className={cn(
      "relative flex flex-col border-r bg-muted/30 transition-all duration-normal ease-industrial",
      isCollapsed ? "w-[64px]" : "w-[240px]"
    )}>
      <div className="flex h-[60px] items-center px-4 border-b">
        <Library className="size-6 text-primary" />
        {!isCollapsed && <span className="ml-3 font-bold tracking-tight text-foreground">AIWF SHARD</span>}
      </div>

      <nav className="flex-1 p-space-2 space-y-1 overflow-y-auto overflow-x-hidden">
        <NavItem icon={LayoutDashboard} label="Overview" isCollapsed={isCollapsed} active />
        <NavItem icon={MessageSquare} label="AI Agents" isCollapsed={isCollapsed} />
        <NavItem icon={Settings} label="Settings" isCollapsed={isCollapsed} />
      </nav>

      <div className="p-space-2 border-t">
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full justify-center"
        >
          {isCollapsed ? <ChevronRight /> : <ChevronLeft />}
        </Button>
      </div>
    </aside>
  )
}

function NavItem({ icon: Icon, label, isCollapsed, active = false }: { icon: any, label: string, isCollapsed: boolean, active?: boolean }) {
  return (
    <div className={cn(
      "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-all hover:bg-accent hover:text-accent-foreground cursor-pointer group",
      active ? "bg-accent text-accent-foreground" : "text-muted-foreground"
    )}>
      <Icon className="size-5 shrink-0" />
      {!isCollapsed && <span className="animate-in fade-in slide-in-from-left-1">{label}</span>}
      {isCollapsed && (
        <div className="absolute left-full ml-2 hidden rounded-md bg-popover px-2 py-1 text-xs text-popover-foreground group-hover:block z-50">
          {label}
        </div>
      )}
    </div>
  )
}
