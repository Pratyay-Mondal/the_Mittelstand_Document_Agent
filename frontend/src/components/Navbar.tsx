"use client";

import { useI18n } from "@/lib/i18n";
import { Languages, Server } from "lucide-react";
import { Button } from "./ui/button";

export function Navbar() {
  const { language, setLanguage, t } = useI18n();

  return (
    <nav className="w-full h-16 bg-background/60 backdrop-blur-md border-b sticky top-0 z-50 flex items-center justify-between px-6">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded bg-primary flex items-center justify-center">
          <Server className="text-primary-foreground w-5 h-5" />
        </div>
        <h1 className="font-semibold text-lg tracking-tight">{t("title")}</h1>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
           <Languages className="w-4 h-4 text-muted-foreground" />
           <Button 
             variant={language === "en" ? "secondary" : "ghost"} 
             size="sm" 
             onClick={() => setLanguage("en")}
           >
             EN
           </Button>
           <Button 
             variant={language === "de" ? "secondary" : "ghost"} 
             size="sm" 
             onClick={() => setLanguage("de")}
           >
             DE
           </Button>
        </div>
      </div>
    </nav>
  );
}
