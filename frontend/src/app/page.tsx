"use client";

import { useI18n } from "@/lib/i18n";
import { FileUpload } from "@/components/FileUpload";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ShieldCheck, Search, Zap } from "lucide-react";
import { Navbar } from "@/components/Navbar";

export default function Home() {
  const { t } = useI18n();

  return (
    <div className="min-h-screen flex flex-col items-center">
      <Navbar />
      
      <main className="flex-1 w-full max-w-5xl px-6 py-24 flex flex-col items-center justify-center gap-16">
        
        {/* Hero Section */}
        <div className="text-center space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-1000">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/20 text-primary text-sm font-medium border border-primary/20 mb-4">
            <Zap className="w-4 h-4" />
            {t("powered_by")}
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/60 leading-tight">
            {t("doc_intel")} <br/> {t("for_the")} <span className="text-primary">Mittelstand</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            {t("tagline")}. {t("hero_subtitle")}
          </p>
        </div>

        {/* Upload Section */}
        <div className="w-full max-w-2xl animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-150">
           <Card className="border-muted bg-card/50 shadow-2xl overflow-hidden backdrop-blur-sm">
             <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent"></div>
             <CardContent className="p-8">
               <FileUpload />
             </CardContent>
           </Card>
        </div>

        {/* Features / Value Props */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full animate-in fade-in duration-1000 delay-300">
          <FeatureCard 
            icon={<Search className="w-6 h-6 text-accent" />}
            title={t("feature1_title")}
            desc={t("feature1_desc")}
          />
          <FeatureCard 
            icon={<ShieldCheck className="w-6 h-6 text-accent" />}
            title={t("feature2_title")}
            desc={t("feature2_desc")}
          />
          <FeatureCard 
            icon={<Zap className="w-6 h-6 text-accent" />}
            title={t("feature3_title")}
            desc={t("feature3_desc")}
          />
        </div>
      </main>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <Card className="bg-card/30 border-muted">
      <CardHeader>
        <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4">
          {icon}
        </div>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{desc}</CardDescription>
      </CardHeader>
    </Card>
  )
}
