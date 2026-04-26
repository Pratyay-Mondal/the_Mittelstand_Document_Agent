"use client";

import { useState, useEffect } from "react";
import { getOriginalExtraction, updateExtraction, reExtract } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { toast } from "sonner";
import { RefreshCw, CheckCircle2, ChevronDown, Edit2, Check } from "lucide-react";
import { ScrollArea } from "./ui/scroll-area";

export function ExtractionPanel({ docId }: { docId: string }) {
  const { t } = useI18n();
  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState<string>("PENDING");
  const [loading, setLoading] = useState(true);

  // Poll for extraction completion if it's pending initially because of background processing
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getOriginalExtraction(docId);
        setData(res.extraction);
        setStatus(res.extraction_status);
        if (res.extraction_status === "PENDING" && !res.extraction) {
          // If totally empty due to bg task, wait and re-fetch
           setTimeout(fetchData, 3000);
        } else {
           setLoading(false);
        }
      } catch (e) {
        console.error(e);
        setLoading(false);
      }
    };
    fetchData();
  }, [docId]);

  const handleUpdate = (key: string, newValue: string) => {
    setData((prev: any) => ({
      ...prev,
      [key]: {
        ...prev[key],
        value: newValue,
      }
    }));
  };

  const handleSave = async () => {
    try {
      await updateExtraction(docId, data);
      setStatus("APPROVED");
      toast.success(t("approved"));
    } catch (e) {
      toast.error(t("error_occurred"));
    }
  };

  const handleReExtract = async () => {
    setLoading(true);
    setStatus("PENDING");
    try {
      await reExtract(docId);
      toast.success("Re-extraction started");
      setTimeout(() => window.location.reload(), 3000); // Simplistic polling
    } catch (e) {
      toast.error("Failed to re-extract");
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center h-full text-muted-foreground gap-4">
        <RefreshCw className="w-8 h-8 animate-spin text-primary" />
        <p>Extracting data natively via Llama 3...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-background">
      <div className="p-4 border-b border-border flex items-center justify-between bg-card text-card-foreground">
        <div>
          <h2 className="font-semibold">Extracted Data</h2>
          <div className="flex items-center gap-2 mt-1">
             <Badge variant={status === "APPROVED" ? "default" : "outline"} className={status === "APPROVED" ? "bg-green-600 hover:bg-green-600" : "border-amber-500 text-amber-500"}>
               {status === "APPROVED" ? t("approved") : t("pending_review")}
             </Badge>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleReExtract}>
            <RefreshCw className="w-4 h-4 mr-2" /> {t("re_extract")}
          </Button>
          <Button size="sm" onClick={handleSave} className="bg-primary hover:bg-primary/90">
             <CheckCircle2 className="w-4 h-4 mr-2" /> {t("approve_all")}
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4 pb-12">
          {data && Object.keys(data).map(key => {
            const field = data[key];
            if (!field) return null;
            return (
              <ExtractionFieldRow 
                key={key} 
                fieldKey={key} 
                field={field} 
                onChange={(val) => handleUpdate(key, val)}
                t={t}
              />
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
}

function ExtractionFieldRow({ fieldKey, field, onChange, t }: { fieldKey: string, field: any, onChange: (v: string) => void, t: any }) {
  const [isEditing, setIsEditing] = useState(false);
  const val = field.value || "";
  const conf = field.confidence || 0;
  
  let confColor = "bg-green-500/20 text-green-500 border-green-500/20";
  let confText = t("confidence_high");
  if (conf < 0.7) {
    confColor = "bg-destructive/20 text-destructive border-destructive/20";
    confText = t("confidence_low");
  } else if (conf < 0.9) {
    confColor = "bg-amber-500/20 text-amber-500 border-amber-500/20";
    confText = t("confidence_medium");
  }

  // Map backend key to i18n
  const labelKey = fieldKey as keyof typeof t;
  const displayLabel = t(labelKey) !== labelKey ? t(labelKey) : fieldKey.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());

  return (
    <Card className={`border ${conf < 0.7 && !isEditing ? 'border-destructive/50 ring-1 ring-destructive/20' : 'border-border'} shadow-sm transition-all`}>
      <CardContent className="p-3">
        <div className="flex items-center justify-between mb-2">
          <Label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">{displayLabel}</Label>
          <Badge variant="outline" className={`text-[10px] py-0 h-4 px-1.5 font-medium ${confColor}`}>
            {confText} {(conf * 100).toFixed(0)}%
          </Badge>
        </div>
        <div className="flex items-end gap-2">
           {isEditing ? (
             <div className="flex-1 flex items-center gap-2">
                <Input 
                  value={val} 
                  onChange={(e) => onChange(e.target.value)} 
                  className="h-8 text-sm"
                  autoFocus
                />
                <Button size="icon" variant="ghost" className="h-8 w-8 text-green-500" onClick={() => setIsEditing(false)}>
                  <Check className="w-4 h-4" />
                </Button>
             </div>
           ) : (
             <div className="flex-1 flex items-center justify-between group cursor-text" onClick={() => setIsEditing(true)}>
                <p className="text-sm font-medium leading-none min-h-6 py-1 select-all">{val || <span className="text-muted-foreground italic">Needs Human Input</span>}</p>
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground">
                    <span className="text-xs">Review</span>
                    <Edit2 className="w-3.5 h-3.5" />
                </div>
             </div>
           )}
        </div>
      </CardContent>
    </Card>
  )
}
