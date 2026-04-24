"use client"
import * as React from "react"
import { Button } from "@/components/ui/button"
import { Bell, Search, Command, User } from "lucide-react"

export function Header() {
  return (
    <header className="flex h-[60px] items-center justify-between border-b bg-background/95 backdrop-blur px-6 z-10">
      <div className="flex items-center gap-4 flex-1">
        <div className="relative w-full max-w-[400px] hidden md:block">
          <Search className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
          <div className="flex h-9 w-full items-center rounded-md border border-input bg-muted/50 px-9 text-sm text-muted-foreground">
            Search Shard...
            <kbd className="pointer-events-none absolute right-2.5 top-2 hidden h-5 select-none items-center gap-1 rounded border bg-background px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
              <Command className="size-3" />K
            </kbd>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="size-5" />
          <span className="absolute top-2 right-2 size-2 rounded-full bg-primary border-2 border-background" />
        </Button>
        <div className="h-8 w-[1px] bg-border mx-1" />
        <Button variant="ghost" size="sm" className="gap-2 px-2">
          <div className="size-8 rounded-full bg-accent flex items-center justify-center">
            <User className="size-4 text-accent-foreground" />
          </div>
          <span className="hidden lg:block text-xs font-semibold">Dorgham (Admin)</span>
        </Button>
      </div>
    </header>
  )
}
