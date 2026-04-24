"use client"
import * as React from "react"
import { Button } from "@/components/ui/button"
import { useTranslations } from "next-intl"

export function Hero() {
  const t = useTranslations("Index")

  return (
    <section className="relative overflow-hidden py-space-16 lg:py-space-24">
      <div className="container relative z-10 mx-auto px-4 text-center">
        <h1 className="animate-in fade-in slide-in-from-bottom-4 duration-slow text-4xl font-extrabold tracking-tight sm:text-6xl lg:text-7xl">
          {t("title")}
        </h1>
        <p className="mx-auto mt-space-6 max-w-2xl text-lg text-muted-foreground animate-in fade-in slide-in-from-bottom-6 duration-slow delay-150">
          {t("description")}
        </p>
        <div className="mt-space-10 flex flex-wrap justify-center gap-4 animate-in fade-in slide-in-from-bottom-8 duration-slow delay-300">
          <Button size="lg" className="rounded-full px-space-8 shadow-premium hover:scale-105 active:scale-95 transition-transform">
            {t("cta")}
          </Button>
          <Button variant="outline" size="lg" className="rounded-full px-space-8">
            View Roadmap
          </Button>
        </div>
      </div>
      
      {/* Background Decorative Elements */}
      <div className="absolute top-0 left-1/2 -z-10 h-full w-full -translate-x-1/2 blur-3xl opacity-20">
        <div className="absolute top-0 left-1/4 h-64 w-64 rounded-full bg-primary" />
        <div className="absolute bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-accent" />
      </div>
    </section>
  )
}
