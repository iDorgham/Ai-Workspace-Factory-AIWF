"use client"
import * as React from "react"
import { cn } from "@/lib/utils"

interface LegalEvent {
  id: string
  date: string
  title: string
  description: string
  status: "COMPLETED" | "PENDING" | "UPCOMING"
}

export function LegalTimeline({ events }: { events: LegalEvent[] }) {
  return (
    <div className="space-y-space-8 p-space-6 bg-card rounded-premium shadow-premium border border-border">
      <h3 className="text-xl font-bold tracking-tight mb-space-4">Case Timeline</h3>
      <div className="relative border-l-2 border-primary ml-space-4">
        {events.map((event, index) => (
          <div key={event.id} className="mb-space-10 ml-space-6 animate-in fade-in slide-in-from-left-4 duration-slow" style={{ animationDelay: `${index * 100}ms` }}>
            <span className="absolute -left-space-2.5 flex h-5 w-5 items-center justify-center rounded-full bg-primary ring-8 ring-background" />
            <time className="text-sm font-normal leading-none text-muted-foreground">{event.date}</time>
            <h4 className="text-lg font-semibold mt-space-1">{event.title}</h4>
            <p className="mt-space-2 text-base text-muted-foreground">{event.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
