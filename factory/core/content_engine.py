import json
import os
from datetime import datetime

class ContentEngine:
    """
    Industrial Content Engine v2.0 for AIWF.
    Orchestrates high-fidelity creative assembly with:
    - Multi-locale support (EN, AR-EG)
    - Section-based folder architecture
    - Aggregated full-page generation
    - Legal compliance root nodes
    """

    def __init__(self, spec_dir="plan/11-website-content/"):
        self.spec_dir = spec_dir
        self.output_root = "workspaces/sovereign-web/"
        self.locales = ["en", "ar-eg"]
        self.specs = {}

    def load_specs(self):
        """Loads refined industrial specs."""
        spec_files = {
            "sitemap": "sitemap-architecture.spec.json",
            "sections": "section-architecture.spec.json",
            "multi": "multilingual-strategy.spec.json",
            "components": "component-content.spec.json"
        }
        try:
            for key, filename in spec_files.items():
                with open(f"{self.spec_dir}{filename}", 'r') as f:
                    self.specs[key] = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading specs: {e}")
            return False

    def get_placeholder(self, component, locale):
        """Mock AI content generator for bilingual sections."""
        data = {
            "en": {
                "hero": "# Industrial SaaS Production\nBuilt for Sovereign Shards.",
                "stats": "## Our Impact\n252+ Agents Active Globally.",
                "legal": "# Legal Protocol\nThis page enforces Law 151 compliance.",
                "cta": "### Start Your Phase\n[Deploy Shard Now]"
            },
            "ar-eg": {
                "hero": "# الإنتاج الصناعي للبرمجيات\nمصمم للسيادة الرقمية الإقليمية.",
                "stats": "## تأثيرنا\nأكثر من ٢٥٢ وكيل ذكي نشط عالمياً.",
                "legal": "# البروتوكول القانوني\nهذه الصفحة تفرض الامتثال للقانون ١٥١ لسنة ٢٠٢٠.",
                "cta": "### ابدأ مرحلتك الآن\n[نشر الشظية البرمجية]"
            }
        }
        # Fallback logic
        base_comp = component.split('-')[1] if '-' in component else component
        return data.get(locale, data['en']).get(base_comp, f"# {component.title()}\nContent pending implementation for {locale}.")

    def assemble_page(self, page_name, parent_dir):
        """Assembles a page folder with section files and a full-page aggregation."""
        page_slug = page_name.lower().replace(" ", "_")
        page_path = os.path.join(parent_dir, page_slug)
        os.makedirs(page_path, exist_ok=True)
        
        sections = self.specs['sections']['page_composition'].get(page_name, ["01-default-content"])
        
        for locale in self.locales:
            locale_path = os.path.join(page_path, locale)
            os.makedirs(locale_path, exist_ok=True)
            
            aggregated_content = f"--- \nTitle: {page_name} ({locale})\nDate: {datetime.now().isoformat()}\n--- \n\n"
            
            for section in sections:
                section_file = f"{section}.md"
                section_content = self.get_placeholder(section, locale)
                
                with open(os.path.join(locale_path, section_file), 'w') as f:
                    f.write(section_content)
                
                aggregated_content += f"\n\n<!-- Section: {section} -->\n{section_content}\n"
            
            with open(os.path.join(locale_path, "full-page.md"), 'w') as f:
                f.write(aggregated_content)
            
            print(f"Assembled page: {page_name} [{locale}]")

    def execute(self):
        """Main execution loop for /content creative assembly."""
        if not self.load_specs():
            return False

        # 1. Sitemap Root Documentation
        os.makedirs(self.output_root, exist_ok=True)
        with open(os.path.join(self.output_root, "sitemap.md"), 'w') as f:
            f.write("# 🌐 AIWF Sovereign Sitemap\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write("**Industrial Status:** PROCESSED\n\n")
            f.write("## 🏗️ Content Shards\n")
            
            for root, dirs, files in os.walk(self.output_root):
                if ".DS_Store" in files: files.remove(".DS_Store")
                level = root.replace(self.output_root, '').count(os.sep)
                indent = '  ' * level
                folder_name = os.path.basename(root)
                if folder_name and folder_name != "sovereign-web":
                    f.write(f"{indent}- **{folder_name}/**\n")
                    for file in sorted(files):
                        if file != "sitemap.md":
                            f.write(f"{indent}  - [{file}](file://{os.path.join(root, file)})\n")

        # 2. Iterate through Hierarchy
        for node in self.specs['sitemap'].get('root_nodes', []):
            for root_name, children in node.items():
                # Root categories like Home, Legal, etc.
                root_path = self.output_root if root_name.lower() == "home" else os.path.join(self.output_root, root_name.lower())
                os.makedirs(root_path, exist_ok=True)
                
                # If Home, we treat it specially (root content)
                if root_name.lower() == "home":
                    self.assemble_page("Home", self.output_root)
                    for child in children:
                        self.assemble_page(child, self.output_root)
                else:
                    # Categorized folders like /legal/ or /documentation/
                    for child in children:
                        self.assemble_page(child, root_path)
        
        print("\n✅ High-Fidelity Creative Assembly Complete.")
        return True

if __name__ == "__main__":
    engine = ContentEngine()
    engine.execute()
