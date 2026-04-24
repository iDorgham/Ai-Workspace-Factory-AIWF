"use client"
import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { MessageSquare, X, Maximize2, Send } from "lucide-react"

export function PersistentChat() {
  const [isOpen, setIsOpen] = React.useState(false)

  return (
    <div className={cn(
      "fixed bottom-6 right-6 z-50 flex flex-col transition-all duration-normal ease-industrial shadow-premium",
      isOpen ? "w-[380px] h-[520px]" : "w-[56px] h-[56px]"
    )}>
      {!isOpen ? (
        <Button 
          size="icon" 
          className="size-14 rounded-full bg-primary shadow-lg hover:scale-105 active:scale-95 transition-transform"
          onClick={() => setIsOpen(true)}
        >
          <MessageSquare className="size-6" />
        </Button>
      ) : (
        <div className="flex flex-col h-full bg-background border rounded-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
          <div className="flex items-center justify-between p-4 border-b bg-muted/30">
            <div className="flex items-center gap-3">
              <div className="size-8 rounded-full bg-primary flex items-center justify-center">
                <MessageSquare className="size-4 text-primary-foreground" />
              </div>
              <div>
                <p className="text-sm font-bold">Orchestrator</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-widest">Active Agent</p>
              </div>
            </div>
            <div className="flex gap-1">
              <Button variant="ghost" size="icon" className="size-8">
                <Maximize2 className="size-4" />
              </Button>
              <Button variant="ghost" size="icon" className="size-8" onClick={() => setIsOpen(false)}>
                <X className="size-4" />
              </Button>
            </div>
          </div>

          <div className="flex-1 p-4 space-y-4 overflow-y-auto">
            <div className="bg-muted p-3 rounded-lg text-sm max-w-[85%] animate-message-pop">
              Hello Dorgham. The dashboard shell is now active. How can I assist with shard materialization today?
            </div>
          </div>

          <div className="p-4 border-t bg-muted/10">
            <div className="flex gap-2">
              <div className="flex-1 bg-background border rounded-lg px-3 py-2 text-sm text-muted-foreground">
                Query agent...
              </div>
              <Button size="icon" className="size-9 shrink-0">
                <Send className="size-4" />
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
