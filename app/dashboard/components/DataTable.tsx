"use client"
import * as React from "react"
import { cn } from "@/lib/utils"

export function DataTable({ data, columns }: { data: any[], columns: any[] }) {
  return (
    <div className="rounded-md border bg-background overflow-hidden shadow-sm">
      <table className="w-full text-sm">
        <thead className="bg-muted/50 border-b">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="h-10 px-4 text-left align-middle font-semibold text-muted-foreground rtl:text-right">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y">
          {data.map((row, i) => (
            <tr key={i} className="hover:bg-muted/30 transition-colors">
              {columns.map((col) => (
                <td key={col.key} className="p-4 align-middle">
                  {row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
