"use client";

import { Company } from "@/types/company";

interface CompanyInfoProps {
  company: Company;
}

export default function CompanyInfo({ company }: CompanyInfoProps) {
  return (
    <div className="card card-hover p-6 animate-fadeIn">
      <div className="border-b border-gray-200 pb-4 mb-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{company.name}</h2>
            <p className="text-lg text-gray-600 mt-1">
              銘柄コード: {company.stock_code}
            </p>
          </div>
          {company.industry && (
            <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
              {company.industry}
            </span>
          )}
        </div>
      </div>

      {company.description && (
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-gray-900">事業内容</h3>
          <p className="text-gray-700 leading-relaxed">{company.description}</p>
        </div>
      )}

      {!company.description && (
        <p className="text-gray-500 italic">事業内容の情報がありません</p>
      )}
    </div>
  );
}
