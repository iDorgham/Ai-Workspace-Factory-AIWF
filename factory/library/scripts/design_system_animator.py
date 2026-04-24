import os

def generate_animations(motion_tokens_path, output_css_path):
    """
    Generates industrial keyframes (fade-in, slide-up, message-pop) 
    synchronized with motion tokens.
    """
    print("🎬 Generating Design System Animations...")
    
    keyframes = """
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { transform: translateY(var(--space-4)); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes message-pop {
  0% { transform: scale(0.9); opacity: 0; }
  70% { transform: scale(1.02); }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes typing-dot {
  0%, 100% { transform: translateY(0); opacity: 0.5; }
  50% { transform: translateY(-3px); opacity: 1; }
}
"""
    with open(output_css_path, 'a') as f:
        f.write(keyframes)
    print(f"✅ Animations appended to {output_css_path}")

if __name__ == "__main__":
    generate_animations("", "factory/library/02-web-platforms/sovereign-ui/tokens.css")
