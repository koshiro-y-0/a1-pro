"use client";

import { useState, useEffect, useCallback } from "react";
import { CompanySearchResult } from "@/types/company";
import { companiesApi } from "@/services/api";

interface SearchBarProps {
  onSelectCompany?: (company: CompanySearchResult) => void;
}

export default function SearchBar({ onSelectCompany }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<CompanySearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  // デバウンス処理
  useEffect(() => {
    if (query.length === 0) {
      setResults([]);
      setShowResults(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const searchResults = await companiesApi.search(query);
        setResults(searchResults);
        setShowResults(true);
      } catch (error) {
        console.error("Search error:", error);
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    }, 300); // 300ms デバウンス

    return () => clearTimeout(timer);
  }, [query]);

  const handleSelectCompany = (company: CompanySearchResult) => {
    setQuery("");
    setShowResults(false);
    if (onSelectCompany) {
      onSelectCompany(company);
    }
  };

  return (
    <div className="relative w-full max-w-2xl">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="銘柄コードまたは企業名を入力..."
          className="input transition-smooth hover:border-primary/50 text-gray-900"
        />
        {isLoading && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
        )}
      </div>

      {/* 検索結果 */}
      {showResults && results.length > 0 && (
        <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto animate-fadeInDown">
          {results.map((company) => (
            <button
              key={company.id}
              onClick={() => handleSelectCompany(company)}
              className="w-full px-4 py-3 text-left hover:bg-blue-50 transition-smooth border-b border-gray-100 last:border-b-0 hover-lift"
            >
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold text-gray-900">
                    {company.stock_code}
                  </span>
                  <span className="ml-2 text-gray-700">{company.name}</span>
                </div>
                {company.industry && (
                  <span className="text-sm text-gray-500">{company.industry}</span>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {/* 検索結果なし */}
      {showResults && results.length === 0 && !isLoading && query.length > 0 && (
        <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg p-4 text-center text-gray-500 animate-fadeInDown">
          該当する銘柄が見つかりませんでした
        </div>
      )}
    </div>
  );
}
