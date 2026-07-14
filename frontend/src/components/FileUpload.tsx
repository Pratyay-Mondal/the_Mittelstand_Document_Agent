"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { UploadCloud, File as FileIcon, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";
import { uploadPdf } from "@/lib/api";

export function FileUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const router = useRouter();
  const { t } = useI18n();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      toast.error("Please upload a PDF document");
      return;
    }

    setIsUploading(true);
    
    try {
      const result = await uploadPdf(file);
      toast.success(t("upload_success"));
      router.push(`/document/${result.doc_id}`);
    } catch (err) {
      toast.error(t("error_occurred"));
    } finally {
      setIsUploading(false);
    }
  }, [router, t]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
    maxFiles: 1,
    disabled: isUploading
  });

  return (
    <div 
      {...getRootProps()} 
      className={`
        border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200
        ${isDragActive ? "border-primary bg-primary/10 scale-105" : "border-border hover:border-primary/50 hover:bg-card"}
        ${isUploading ? "opacity-70 cursor-not-allowed" : ""}
      `}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center gap-4">
        {isUploading ? (
          <div className="relative">
            <Loader2 className="w-12 h-12 text-primary animate-spin" />
            <div className="absolute inset-0 rounded-full animate-ping border border-primary opacity-20"></div>
          </div>
        ) : isDragActive ? (
          <FileIcon className="w-12 h-12 text-primary animate-bounce" />
        ) : (
          <UploadCloud className="w-12 h-12 text-muted-foreground" />
        )}
        
        <div className="space-y-1">
          <p className="text-lg font-medium">
            {isUploading ? t("processing") : t("upload_drop")}
          </p>
          {!isUploading && (
            <p className="text-sm text-muted-foreground">
              {t("upload_select")} (Max 10MB)
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
