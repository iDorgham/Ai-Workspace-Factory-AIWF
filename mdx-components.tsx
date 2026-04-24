import type { MDXComponents } from 'mdx/types'
import { Button } from '@/components/ui/button'
// Add more Sovereign-UI components here

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h1: ({ children }) => <h1 className="text-4xl font-bold tracking-tight mb-space-4">{children}</h1>,
    h2: ({ children }) => <h2 className="text-3xl font-semibold tracking-tight mb-space-3 mt-space-6">{children}</h2>,
    p: ({ children }) => <p className="leading-7 mb-space-4 text-muted-foreground">{children}</p>,
    Button: (props: any) => <Button {...props} />,
    ...components,
  }
}
